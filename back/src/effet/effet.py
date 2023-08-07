from __future__ import annotations

from dataclasses import dataclass

from back.src.figurine.caracteristique import Caracteristique


@dataclass
class EffetTheorique:
    """
    Gère les effets d'armes, de psychologie, de charge.
    """

    nom: str
    modificateur_carac_allie: Caracteristique
    modificateur_carac_adverse: Caracteristique
    set_nom_effet_necessaire_allie: set[str]
    set_nom_effet_necessaire_adverse: set[str]
    set_nom_effet_suppresseur_allie: set[str]
    set_nom_effet_suppresseur_adverse: set[str]
    set_nom_effet_inclu: set[str]

    def is_valide(
        self,
        liste_nom_effet_allie: list[str],
        liste_nom_effet_adverse: list[str],
    ) -> bool:
        """
        Vérifie si l'effet est valide avec les deux listes données.
        """
        if not set(self.set_nom_effet_necessaire_allie).issubset(
            set(liste_nom_effet_allie)
        ):
            return False
        if not set(self.set_nom_effet_necessaire_adverse).issubset(
            set(liste_nom_effet_adverse)
        ):
            return False
        if set(self.set_nom_effet_suppresseur_allie) & set(liste_nom_effet_allie):
            return False
        if set(self.set_nom_effet_suppresseur_adverse) & set(liste_nom_effet_adverse):
            return False
        return True


# @dataclass
# class ListEffetFigurine:
#     liste_effet: list[Effet]

#     def get_list_effet_valide(self):
#         pass

#     def ajout_effet(self):
#         pass
