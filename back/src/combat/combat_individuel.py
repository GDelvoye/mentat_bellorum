from typing import Optional

from back.src.combat.attaque import AttaqueCac
from back.src.figurine.caracteristique import Caracteristique


def jet_pour_toucher_cac(capa_combat_attaquant: int, capa_combat_defenseur: int) -> int:
    """Tableau des jets pour toucher au corps à corps."""
    if capa_combat_attaquant > capa_combat_defenseur:
        return 3
    elif capa_combat_defenseur < 2 * capa_combat_attaquant:
        return 4
    else:
        return 5


def jet_pour_blesser(force_attaquant: int, endurance_defenseur: int) -> Optional[int]:
    """Tableau des jets pour blesser."""
    if force_attaquant >= endurance_defenseur + 2:
        return 2
    elif force_attaquant == endurance_defenseur + 1:
        return 3
    elif force_attaquant == endurance_defenseur:
        return 4
    elif force_attaquant + 1 == endurance_defenseur:
        return 5
    elif force_attaquant + 3 >= endurance_defenseur:
        return 6
    return None


def jet_de_sauvegarde(
    force_attaquant: int, sauvegarde_defenseur: int, malus_sauvegarde: int
) -> int:
    """Modification de la sauvegarde d'armure en fonction de la force."""
    force_contre_sauvegarde = force_attaquant + malus_sauvegarde
    if force_contre_sauvegarde <= 3:
        return sauvegarde_defenseur
    else:
        return min(7, sauvegarde_defenseur + force_contre_sauvegarde - 3)


def probabilite_de_toucher_cac(
    capa_combat_attaquant: int, capa_combat_defenseur: int
) -> float:
    return (7 - jet_pour_toucher_cac(capa_combat_attaquant, capa_combat_defenseur)) / 6


def probabilite_de_blesser(force_attaquant: int, endurance_defenseur: int) -> float:
    valeur_pour_blesser = jet_pour_blesser(force_attaquant, endurance_defenseur)
    if valeur_pour_blesser is None:
        return 0
    assert valeur_pour_blesser is not None
    return (7 - valeur_pour_blesser) / 6


def probabilite_de_rater_sa_sauvegarde(
    force_attaquant: int,
    sauvegarde_defenseur: int,
    malus_sauvegarde: int,
) -> float:
    """Si la sauvegarde est de 7, on la rate toujours."""
    valeur_effective_sauvegarde = jet_de_sauvegarde(
        force_attaquant,
        sauvegarde_defenseur,
        malus_sauvegarde,
    )
    return (valeur_effective_sauvegarde - 1) / 6


def probabilite_de_rater_sa_sauvegarde_invunerable(
    sauvegarde_invulnerable_defenseur: int,
) -> float:
    """Si la sauvegarde est de 7, on la rate toujours."""
    valeur_effective_sauvegarde = jet_de_sauvegarde(
        force_attaquant=0,
        sauvegarde_defenseur=sauvegarde_invulnerable_defenseur,
        malus_sauvegarde=0,
    )
    return (valeur_effective_sauvegarde - 1) / 6


def probabilite_une_attaque_fait_perdre_un_point_de_vie(
    attaque: AttaqueCac,
    caracteristique_avec_equipement_defenseur: Caracteristique,
):
    """Probabilité d'infliger la perte d'un point de vie lors d'une attaque cac."""
    probabilite = 1.0
    probabilite *= probabilite_de_toucher_cac(
        attaque.caracteristique.capa_combat,
        caracteristique_avec_equipement_defenseur.capa_combat,
    )
    probabilite *= probabilite_de_blesser(
        attaque.caracteristique.force,
        caracteristique_avec_equipement_defenseur.endurance,
    )
    probabilite *= probabilite_de_rater_sa_sauvegarde(
        attaque.caracteristique.force,
        caracteristique_avec_equipement_defenseur.sauvegarde,
        0,
    )
    probabilite *= probabilite_de_rater_sa_sauvegarde_invunerable(
        caracteristique_avec_equipement_defenseur.sauvegarde_invulnerable,
    )
    return probabilite
