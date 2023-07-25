from typing import Optional


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
