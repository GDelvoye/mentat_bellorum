from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Dependances:
    necessaire_allie: Set[str]
    necessaire_adverse: Set[str]
    suppresseur_allie: Set[str]
    suppresseur_adverse: Set[str]
    effet_inclu: Set[str]

    def all_dependances(self) -> Set[str]:
        all_dependances = set()
        all_dependances.update(self.necessaire_allie)
        all_dependances.update(self.necessaire_adverse)
        all_dependances.update(self.suppresseur_allie)
        all_dependances.update(self.suppresseur_adverse)
        all_dependances.update(self.effet_inclu)
        return all_dependances

    def is_valide_necessaire_allie(self, reference_dependance: Dependances) -> bool:
        if (
            self.necessaire_allie.intersection(reference_dependance.necessaire_allie)
            == reference_dependance.necessaire_allie
        ):
            return True
        else:
            return False

    def is_valide_suppresseur_allie(self, reference_dependance: Dependances) -> bool:
        if (
            self.suppresseur_allie.intersection(reference_dependance.suppresseur_allie)
            == set()
        ):
            return True
        else:
            return False

    def is_valide_suppresseur_adverse(self, reference_dependance: Dependances) -> bool:
        if (
            self.suppresseur_adverse.intersection(
                reference_dependance.suppresseur_adverse
            )
            == set()
        ):
            return True
        else:
            return False

    def is_valide(self, reference_dependance: Dependances) -> bool:
        return bool(
            self.is_valide_necessaire_allie(reference_dependance)
            * self.is_valide_suppresseur_allie(reference_dependance)
            * self.is_valide_suppresseur_adverse(reference_dependance)
        )


@dataclass
class EffetTheorique:
    """
    Gère les effets d'armes, de psychologie, de charge.
    """

    nom: str
    modificateur_carac_allie: Caracteristique
    modificateur_carac_adverse: Caracteristique
    dependances: Dependances

    # def is_valide(
    #     self,
    #     liste_nom_effet_allie: list[str],
    #     liste_nom_effet_adverse: list[str],
    # ) -> bool:
    #     """
    #     Vérifie si l'effet est valide avec les deux listes données.
    #     """
    #     if not set(self.set_nom_effet_necessaire_allie).issubset(
    #         set(liste_nom_effet_allie)
    #     ):
    #         return False
    #     if not set(self.set_nom_effet_necessaire_adverse).issubset(
    #         set(liste_nom_effet_adverse)
    #     ):
    #         return False
    #     if set(self.set_nom_effet_suppresseur_allie) & set(liste_nom_effet_allie):
    #         return False
    #     if set(self.set_nom_effet_suppresseur_adverse) & set(liste_nom_effet_adverse):
    #         return False
    #     return True


class EffetPratique:
    def __init__(self, nom: str):
        self.nom = nom
        self.is_valide: Optional[bool] = None
        self.set_des_effets_pratiques_dependances: Set[EffetPratique] = set()
        self.dependances: Dependances = Dependances(set(), set(), set(), set(), set())

    def __repr__(self):
        return self.nom

    def update_set_effet_pratique_dependances(
        self, liste_effet_pratique: list[EffetPratique]
    ) -> None:
        self.set_des_effets_pratiques_dependances.update(liste_effet_pratique)

    def check_is_valide(
        self, dict_effet_theorique: dict[str, EffetTheorique]
    ) -> Optional[bool]:
        """
        Vérifie récursivement si un effet pratique est valide.
        I.e. Si dans le set de dépendances de l'effet pratique, toutes les
        dépendances théoriques sont vérifiées.
        """
        dict_validite_des_dependances: dict[str, Optional[bool]] = {
            effet_pratique.nom: effet_pratique.check_is_valide(dict_effet_theorique)
            for effet_pratique in self.set_des_effets_pratiques_dependances
        }

        set_dependances_pratiques_valides = get_set_nom_effet_pratique_valide(
            dict_validite_des_dependances
        )

        dependances_pratiques_valide = get_dependances(
            self.nom,
            dict_effet_theorique,
            set_dependances_pratiques_valides,
        )

        effet_theorique: EffetTheorique = dict_effet_theorique[self.nom]
        dependances_theorique = effet_theorique.dependances

        if dependances_pratiques_valide.is_valide(dependances_theorique):
            self.is_valide = True
        else:
            self.is_valide = False

        return self.is_valide


def get_dependances(
    nom: str,
    dict_effet_theorique: dict[str, EffetTheorique],
    set_de_noms_allie: Set[str],
    set_de_noms_adverse: Set[str] = set(),
) -> Dependances:
    effet_theorique: EffetTheorique = dict_effet_theorique[nom]
    dependances_theoriques: Dependances = effet_theorique.dependances
    dependances_pratique = Dependances(
        set(set_de_noms_allie).intersection(dependances_theoriques.necessaire_allie),
        set(),
        set(set_de_noms_allie).intersection(dependances_theoriques.suppresseur_allie),
        set(),
        set(),
    )
    return dependances_pratique


def get_set_nom_effet_pratique_valide(
    dict_validite_des_effet_pratique: dict[str, Optional[bool]],
) -> Set[str]:
    nom_effet_pratique_valide = set()
    for nom, is_valide in dict_validite_des_effet_pratique.items():
        if is_valide:
            nom_effet_pratique_valide.add(nom)
    return nom_effet_pratique_valide


def get_dict_effet_pratique_from_liste_nom(
    set_nom: Set[str],
    dict_effet_theorique: dict[str, EffetTheorique],
) -> dict[str, EffetPratique]:
    dict_effet_pratique = {nom: EffetPratique(nom) for nom in set_nom}
    for nom, effet_pratique in dict_effet_pratique.items():
        effet_pratique.dependances = get_dependances(nom, dict_effet_theorique, set_nom)
        set_noms_dependances_pratiques = effet_pratique.dependances.all_dependances()
        liste_effet_pratique_dependance = [
            dict_effet_pratique[nom] for nom in set_noms_dependances_pratiques
        ]
        effet_pratique.update_set_effet_pratique_dependances(
            liste_effet_pratique_dependance
        )
    return dict_effet_pratique


def get_set_effet_pratique_valide_from_liste_nom(
    set_nom: Set[str],
    dict_effet_theorique: dict[str, EffetTheorique],
) -> Set[str]:
    set_effet_pratique_valide: Set[str] = set()
    dict_effet_pratique = get_dict_effet_pratique_from_liste_nom(
        set_nom, dict_effet_theorique
    )
    for nom, effet_pratique in dict_effet_pratique.items():
        effet_pratique.check_is_valide(dict_effet_theorique)
        if effet_pratique.is_valide:
            set_effet_pratique_valide.add(nom)
    return set_effet_pratique_valide
