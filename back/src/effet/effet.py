from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

from back.src.api.api_dict_effet import get_dict_effet_theorique
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

    def all_dependances_allies(self) -> Set[str]:
        all_dependances_allies = set()
        all_dependances_allies.update(self.necessaire_allie)
        all_dependances_allies.update(self.suppresseur_allie)
        all_dependances_allies.update(self.effet_inclu)
        return all_dependances_allies

    def all_dependances_adverses(self) -> Set[str]:
        all_dependances_adverses = set()
        all_dependances_adverses.update(self.necessaire_adverse)
        all_dependances_adverses.update(self.suppresseur_adverse)
        return all_dependances_adverses

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


class EffetPratique:
    def __init__(self, nom: str):
        self.nom = nom
        self.is_valide: Optional[bool] = None
        self.effets_pratiques_directements_dependants: Set[EffetPratique] = set()
        self.dependances: Dependances = Dependances(set(), set(), set(), set(), set())

    def __repr__(self):
        return self.nom

    def update_ensemble_des_effets_pratiques_directement_dependants(
        self, liste_effet_pratique: list[EffetPratique]
    ) -> None:
        self.effets_pratiques_directements_dependants.update(liste_effet_pratique)

    def check_is_valide(
        self,
    ) -> Optional[bool]:
        """
        Vérifie récursivement si un effet pratique est valide.
        I.e. Si dans le set de dépendances de l'effet pratique, toutes les
        dépendances théoriques sont vérifiées.
        """
        if self.is_valide is not None:
            return self.is_valide

        dict_validite_des_dependances: dict[str, Optional[bool]] = {
            effet_pratique.nom: effet_pratique.check_is_valide()
            for effet_pratique in self.effets_pratiques_directements_dependants
        }

        ensemble_des_noms_directements_dependants_valides = (
            get_noms_valides_from_dict_effet_pratique(dict_validite_des_dependances)
        )

        dependances_pratiques_valide = get_dependances_from_ensembles_noms_effets(
            self.nom,
            ensemble_des_noms_directements_dependants_valides,
            self.dependances.all_dependances_adverses(),
        )
        dict_effet_theorique = get_dict_effet_theorique()
        effet_theorique: EffetTheorique = dict_effet_theorique[self.nom]
        dependances_theorique = effet_theorique.dependances

        if dependances_pratiques_valide.is_valide(dependances_theorique):
            self.is_valide = True
        else:
            self.is_valide = False

        return self.is_valide


def get_dependances_from_ensembles_noms_effets(
    nom: str,
    noms_effets_allies: Set[str],
    noms_effets_adverses: Set[str] = set(),
) -> Dependances:
    """
    Pour un nom d'effet, renvoie une instance de Dependance.
    Cette instance est la Dependance issue de
    noms_effets_allies et noms_effets_adverses et
    compatible avec la Dependance theorique.
    """
    dict_effet_theorique = get_dict_effet_theorique()
    effet_theorique: EffetTheorique = dict_effet_theorique[nom]
    dependances_theoriques: Dependances = effet_theorique.dependances
    dependances_pratique = Dependances(
        noms_effets_allies.intersection(dependances_theoriques.necessaire_allie),
        set(),  # a modifier 2.
        noms_effets_allies.intersection(dependances_theoriques.suppresseur_allie),
        noms_effets_adverses.intersection(dependances_theoriques.suppresseur_adverse),
        set(),  # a modifier 1.
    )
    return dependances_pratique


def get_noms_valides_from_dict_effet_pratique(
    dict_validite_des_effets_pratiques: dict[str, Optional[bool]],
) -> Set[str]:
    noms_effets_pratiques_valides = set()
    for nom, is_valide in dict_validite_des_effets_pratiques.items():
        if is_valide:
            noms_effets_pratiques_valides.add(nom)
    return noms_effets_pratiques_valides


def get_dict_effet_pratique_avant_ckeck_is_valide(
    noms_effets_allies: Set[str],
    noms_effets_adverses: Set[str] = set(),
) -> dict[str, EffetPratique]:
    dict_effet_pratique = {nom: EffetPratique(nom) for nom in noms_effets_allies}
    for nom, effet_pratique in dict_effet_pratique.items():
        effet_pratique.dependances = get_dependances_from_ensembles_noms_effets(
            nom, noms_effets_allies, noms_effets_adverses
        )
        noms_dependances_pratiques_allies = (
            effet_pratique.dependances.all_dependances_allies()
        )
        effets_pratiques_allies_dependants = [
            dict_effet_pratique[nom] for nom in noms_dependances_pratiques_allies
        ]
        effet_pratique.update_ensemble_des_effets_pratiques_directement_dependants(
            effets_pratiques_allies_dependants
        )
    return dict_effet_pratique


def get_ensemble_des_effet_pratique_valide_apres_check(
    noms_effets_allies: Set[str],
    noms_effets_adverses: Set[str] = set(),
) -> Set[str]:
    dict_effet_pratique = get_dict_effet_pratique_avant_ckeck_is_valide(
        noms_effets_allies, noms_effets_adverses
    )
    ensemble_des_effets_valides_apres_check: Set[str] = set()
    for nom, effet_pratique in dict_effet_pratique.items():
        effet_pratique.check_is_valide()
        if effet_pratique.is_valide:
            ensemble_des_effets_valides_apres_check.add(nom)
    return ensemble_des_effets_valides_apres_check
