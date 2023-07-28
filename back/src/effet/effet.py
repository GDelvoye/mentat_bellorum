from __future__ import annotations

from dataclasses import dataclass

from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Effet:
    nom: str
    modificateur_carac_allie: Caracteristique
    modificateur_carac_adverse: Caracteristique
    liste_nom_effet_necessaire_allie: list[str]
    liste_nom_effet_necessaire_adverse: list[str]
    liste_nom_effet_suppresseur_allie: list[str]
    liste_nom_effet_suppresseur_adverse: list[str]

    def is_valide(
        self,
        liste_nom_effet_allie: list[str],
        liste_nom_effet_adverse: list[str],
    ) -> bool:
        """
        Vérifie si l'effet est valide avec les deux listes données.
        """
        if not set(self.liste_nom_effet_necessaire_allie).issubset(
            set(liste_nom_effet_allie)
        ):
            return False
        if not set(self.liste_nom_effet_necessaire_adverse).issubset(
            set(liste_nom_effet_adverse)
        ):
            return False
        if set(self.liste_nom_effet_suppresseur_allie) & set(liste_nom_effet_allie):
            return False
        if set(self.liste_nom_effet_suppresseur_adverse) & set(liste_nom_effet_adverse):
            return False
        return True
