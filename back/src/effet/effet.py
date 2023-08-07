from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

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


class EffetPratique:
    def __init__(self, nom: str):
        self.nom = nom
        self.is_valide: Optional[bool] = None
        self.dependances: Set[EffetPratique] = set()

    def __repr__(self):
        return self.nom

    def add_dependance(self, liste_effet_pratique: list[EffetPratique]) -> None:
        self.dependances.update(liste_effet_pratique)

    def check_is_valide(self, dict_effet_theorique: dict[str, EffetTheorique]) -> None:
        """
        Vérifie récursivement si un effet pratique est valide.
        I.e. Si dans le set de dépendances de l'effet pratique, toutes les
        dépendances théoriques sont vérifiées.
        """
        dict_validite_des_dependances_directes: dict[str, Optional[bool]] = {
            effet_pratique.nom: effet_pratique.check_is_valide()
            for effet_pratique in self.dependances
        }
        # print("------------")
        # print(f"{self}: {dict_nodes}")
        set_dependances_pratiques_directes_valides = set()
        # u = set(dict_nodes.keys())
        for nom, is_valide in dict_validite_des_dependances_directes.items():
            if is_valide:
                set_dependances_pratiques_directes_valides.add(nom)
        effet_theorique: EffetTheorique = dict_effet_theorique[self.nom]
        set_dependances_theoriques_directes = (
            effet_theorique.set_nom_effet_necessaire_allie
        )
        # diff = set_dependances_pratiques_directes_valides.difference(set_dependances_theoriques_directes)
        if (
            set_dependances_pratiques_directes_valides.difference(
                set_dependances_theoriques_directes
            )
            == set()
            and set_dependances_theoriques_directes.difference(
                set_dependances_pratiques_directes_valides
            )
            == set()
        ):
            for dependance in self.dependances:
                #  print("uuu")
                #  print(node.nom)
                if dependance.is_valide is False:
                    self.is_valide = False
            self.is_valide = True
        else:
            self.is_valide = False
        # print(f"{self}::: u={u_true}, s={s_theoric}, diff={diff}, is_valide={self.is_valide}")

        return self.is_valide


def get_set_dependances_pratiques_directes_from_liste_nom(
    nom: str,
    liste_nom: list[str],
    dict_effet_theorique: dict[str, EffetTheorique],
):
    effet_theorique: EffetTheorique = dict_effet_theorique[nom]
    set_dependance = set(liste_nom).intersection(
        effet_theorique.set_nom_effet_necessaire_allie
    )
    return set_dependance


def get_dict_effet_pratique_from_liste_nom(
    liste_nom: list[str],
    dict_effet_theorique: dict[str, EffetTheorique],
):
    dict_effet_pratique = {nom: EffetPratique(nom) for nom in liste_nom}
    for nom, effet_pratique in dict_effet_pratique.items():
        set_dependances_pratiques = (
            get_set_dependances_pratiques_directes_from_liste_nom(
                nom, liste_nom, dict_effet_theorique
            )
        )
        liste_dependance_effective = [
            dict_effet_pratique[nom] for nom in set_dependances_pratiques
        ]
        effet_pratique.add_dependance(liste_dependance_effective)
    return dict_effet_pratique


# @dataclass
# class ListEffetFigurine:
#     liste_effet: list[Effet]

#     def get_list_effet_valide(self):
#         pass

#     def ajout_effet(self):
#         pass
