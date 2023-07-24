import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass

from back.src.combat.attaque import AttaqueCac
from back.src.effet.effet import Effet
from back.src.equipement.arme.arme import Arme
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Socle:
    longueur: float
    largeur: float


@dataclass
class Figurine(ABC):
    nom: str
    caracteristique_de_base: Caracteristique
    liste_arme: list[Arme]
    liste_effet: list[Effet]
    socle: Socle

    @abstractmethod
    def liste_attaque(self, liste_arme: list[Arme]) -> list[AttaqueCac]:
        pass


@dataclass
class Fantassin(Figurine):
    def liste_attaque(self, liste_arme: list[Arme]) -> list[AttaqueCac]:
        liste_attaque = []
        caracteristique_avec_equipement = copy.deepcopy(self.caracteristique_de_base)
        for arme in liste_arme:
            caracteristique_avec_equipement = caracteristique_avec_equipement.ajout(
                arme.modification_caracteristique
            )
        nombre_attaque = caracteristique_avec_equipement.attaque
        for i in range(0, nombre_attaque):
            liste_attaque.append(
                AttaqueCac(
                    caracteristique_avec_equipement,
                    self.liste_effet + arme.liste_effet,
                )
            )
        return liste_attaque


class Champion(Fantassin):
    pass
