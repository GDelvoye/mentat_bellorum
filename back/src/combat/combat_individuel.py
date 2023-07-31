from typing import Optional

from back.base_logger import logger
from back.src.combat.attaque import AttaqueCac
from back.src.figurine.caracteristique import Caracteristique
from back.src.parser.type import EnumEffet


def probabilite_relance(probabilite: float) -> float:
    return probabilite + (1 - probabilite) * probabilite


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


def dict_probabilite_attaque_empoisonne(
    attaque: AttaqueCac,
    caracteristique_avec_equipement_defenseur: Caracteristique,
) -> dict[int, float]:
    logger.info(EnumEffet.attaque_empoisonnee.value)
    probabilite_toucher = probabilite_de_toucher_cac(
        attaque.caracteristique.capa_combat,
        caracteristique_avec_equipement_defenseur.capa_combat,
    )
    probabilite_toucher_poison = 1 / 6
    probabilite_toucher_normal = probabilite_toucher - probabilite_toucher_poison
    logger.info(f"toucher: {probabilite_toucher_normal}")
    probabilite_de_blesser_normal = probabilite_de_blesser(
        attaque.caracteristique.force,
        caracteristique_avec_equipement_defenseur.endurance,
    )
    logger.info(f"blesser: {probabilite_de_blesser_normal}")

    probabilite_de_blesser_empoisonnement = 1

    probabilite_blesser = (
        probabilite_toucher_normal * probabilite_de_blesser_normal
        + probabilite_toucher_poison * probabilite_de_blesser_empoisonnement
    )
    logger.info(f"toucher/blesser tot {probabilite_blesser}")

    probabilite_final = (
        probabilite_blesser
        * probabilite_de_rater_sa_sauvegarde(
            attaque.caracteristique.force,
            caracteristique_avec_equipement_defenseur.sauvegarde,
            0,
        )
        * probabilite_de_rater_sa_sauvegarde_invunerable(
            caracteristique_avec_equipement_defenseur.sauvegarde_invulnerable,
        )
    )
    logger.info(f"final: {probabilite_final}")

    return {
        1: probabilite_final,
    }


def dict_probabilite_coup_fatal(
    attaque: AttaqueCac,
    caracteristique_avec_equipement_defenseur: Caracteristique,
) -> dict[int, float]:
    probabilite = 1.0

    probabilite *= probabilite_de_toucher_cac(
        attaque.caracteristique.capa_combat,
        caracteristique_avec_equipement_defenseur.capa_combat,
    )

    probabilite_de_blesser_classique = probabilite_de_blesser(
        attaque.caracteristique.capa_combat,
        caracteristique_avec_equipement_defenseur.endurance,
    )

    probabilite_de_blesser_sans_6 = max(0, probabilite_de_blesser_classique - 1 / 6)

    probabilite_sans_coup_fatal = (
        probabilite
        * probabilite_de_blesser_sans_6
        * probabilite_de_rater_sa_sauvegarde(
            attaque.caracteristique.force,
            caracteristique_avec_equipement_defenseur.sauvegarde,
            0,
        )
        * probabilite_de_rater_sa_sauvegarde_invunerable(
            caracteristique_avec_equipement_defenseur.sauvegarde_invulnerable,
        )
    )

    probabilite_avec_coup_fatal = (
        probabilite
        * 1
        / 6
        * probabilite_de_rater_sa_sauvegarde_invunerable(
            caracteristique_avec_equipement_defenseur.sauvegarde_invulnerable,
        )
    )

    return {
        1: probabilite_sans_coup_fatal,
        caracteristique_avec_equipement_defenseur.point_de_vie: probabilite_avec_coup_fatal,
    }


def dict_probabilite_attaque_enflammee_contre_inflammable(
    attaque: AttaqueCac,
    caracteristique_avec_equipement_defenseur: Caracteristique,
) -> dict[int, float]:
    logger.info(EnumEffet.attaque_enflammee.value)
    probabilite_toucher = probabilite_de_toucher_cac(
        attaque.caracteristique.capa_combat,
        caracteristique_avec_equipement_defenseur.capa_combat,
    )
    probabilite_de_blesser_normal = probabilite_de_blesser(
        attaque.caracteristique.force,
        caracteristique_avec_equipement_defenseur.endurance,
    )
    logger.info(f"blesser: {probabilite_de_blesser_normal}")

    probabilite_blesser = probabilite_relance(probabilite_de_blesser_normal)
    logger.info(f"blesser inflammable: {probabilite_blesser}")

    probabilite_final = (
        probabilite_toucher
        * probabilite_blesser
        * probabilite_de_rater_sa_sauvegarde(
            attaque.caracteristique.force,
            caracteristique_avec_equipement_defenseur.sauvegarde,
            0,
        )
        * probabilite_de_rater_sa_sauvegarde_invunerable(
            caracteristique_avec_equipement_defenseur.sauvegarde_invulnerable,
        )
    )
    logger.info(f"final: {probabilite_final}")

    return {
        1: probabilite_final,
    }


def dict_nb_pv_perdu_probabilite(
    attaque: AttaqueCac,
    caracteristique_avec_equipement_defenseur: Caracteristique,
    liste_nom_effet_valide_attaquant: list[str],
    liste_nom_effet_valide_defenseur: list[str],
) -> dict[int, float]:
    """Probabilité d'infliger la perte d'un point de vie lors d'une attaque cac."""
    if EnumEffet.attaque_empoisonnee.value in liste_nom_effet_valide_attaquant:
        logger.info(EnumEffet.attaque_empoisonnee.value)
        return dict_probabilite_attaque_empoisonne(
            attaque,
            caracteristique_avec_equipement_defenseur,
        )
    elif EnumEffet.coup_fatal.value in liste_nom_effet_valide_attaquant:
        logger.info(EnumEffet.coup_fatal.value)
        return dict_probabilite_coup_fatal(
            attaque,
            caracteristique_avec_equipement_defenseur,
        )
    elif (
        EnumEffet.attaque_enflammee.value in liste_nom_effet_valide_attaquant
        and EnumEffet.inflammable.value in liste_nom_effet_valide_defenseur
    ):
        logger.info(EnumEffet.attaque_enflammee.value)
        return dict_probabilite_attaque_enflammee_contre_inflammable(
            attaque,
            caracteristique_avec_equipement_defenseur,
        )

    else:
        return {
            1: probabilite_une_attaque_fait_perdre_un_point_de_vie(
                attaque,
                caracteristique_avec_equipement_defenseur,
            )
        }
