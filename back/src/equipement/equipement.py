from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum

from back.src.effet.effet import EffetTheorique
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Equipement(ABC):
    nom: str
    modification_caracteristique: Caracteristique
    liste_effet: list[EffetTheorique]


class TypeEquipement(Enum):
    arme = 1
    armure = 2


@dataclass
class Armure(Equipement):
    type_equipement = TypeEquipement.armure


class TypeArme(Enum):
    arme_base = 1
    arme_une_main = 2
    arme_deux_mains = 3
    arme_tir = 4
    bouclier = 5


@dataclass
class Arme(Equipement):
    liste_effet_necessaire_allie: list[EffetTheorique]
    type_arme: TypeArme
    type_equipement = TypeEquipement.arme


def is_liste_arme_valid(liste_arme: list[Arme]) -> bool:
    """
    Valide ou non l'equipement.
    """
    if len(liste_arme) == 0:
        return False
    if len(liste_arme) == 1:
        if liste_arme[0].type_arme == TypeArme.bouclier:
            return False
        else:
            return True
    if len(liste_arme) > 2:
        return False
    arme1, arme2 = liste_arme
    if (arme1.type_arme or arme2.type_arme) == TypeArme.arme_deux_mains:
        return False
    return True
