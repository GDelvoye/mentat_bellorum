from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from back.src.combat.attaque import AttaqueCac
from back.src.effet.effet import Effet
from back.src.equipement.equipement import Arme, Armure, is_liste_arme_valid
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Socle:
    longueur: float
    largeur: float


@dataclass
class Figurine:
    nom: str
    caracteristique_de_base: Caracteristique
    liste_arme: list[Arme]
    armure: Armure
    liste_effet: list[Effet]
    socle: Socle

    @abstractmethod
    def avec_equipement(self, liste_arme: list[Arme]) -> Optional[FigurineEquipee]:
        pass

    def get_dict_effet_intrinseque(self, liste_arme: list[Arme]) -> dict[str, Effet]:
        dict_intrinseque = {}
        for effet in self.liste_effet:
            dict_intrinseque[effet.nom] = effet
        if self.armure != []:
            for effet in self.armure.liste_effet:
                dict_intrinseque[effet.nom] = effet
        for arme in liste_arme:
            for effet in arme.liste_effet:
                dict_intrinseque[effet.nom] = effet
        return dict_intrinseque

    def get_caracteristique_intrinseque(
        self, liste_arme: list[Arme]
    ) -> Caracteristique:
        carac_intrinseque = self.get_caracteristique_avec_equipement(liste_arme)
        dict_effet_intrinseque = self.get_dict_effet_intrinseque(liste_arme)
        for effet in dict_effet_intrinseque.values():
            carac_intrinseque += effet.modificateur_carac_allie
        return carac_intrinseque

    def get_modification_caracteristique_adverse_intrinseque(
        self,
        liste_arme: list[Arme],
    ) -> Caracteristique:
        modif_carac_intrinseque = Caracteristique()
        dict_effet_intrinseque = self.get_dict_effet_intrinseque(liste_arme)
        for effet in dict_effet_intrinseque.values():
            modif_carac_intrinseque += effet.modificateur_carac_adverse
        return modif_carac_intrinseque

    def get_caracteristique_avec_equipement(
        self, liste_arme: list[Arme]
    ) -> Caracteristique:
        caracteristique_avec_equipement = copy.deepcopy(self.caracteristique_de_base)
        if self.armure != []:
            caracteristique_avec_equipement += self.armure.modification_caracteristique
        for arme in liste_arme:
            caracteristique_avec_equipement += arme.modification_caracteristique
        return caracteristique_avec_equipement

    def get_liste_effet_avec_equipement(self, liste_arme: list[Arme]) -> list[Effet]:
        liste_effet_avec_equipement = self.liste_effet.copy()
        if self.armure != []:
            liste_effet_avec_equipement += self.armure.liste_effet
        for arme in liste_arme:
            liste_effet_avec_equipement += arme.liste_effet
        return liste_effet_avec_equipement

    def get_caracteristique_effective(
        self, liste_arme_valide: list[Arme]
    ) -> Caracteristique:
        caracteristique_effective = self.get_caracteristique_avec_equipement(
            liste_arme_valide
        )
        for effet in self.liste_effet:
            caracteristique_effective += effet.modificateur_carac_allie
        return caracteristique_effective

    def get_liste_attaque(self, liste_arme: list[Arme]) -> list[AttaqueCac]:
        if is_liste_arme_valid(liste_arme):
            caracteristique_avec_equipement = self.get_caracteristique_avec_equipement(
                liste_arme
            )
            liste_effet_avec_equipement = self.get_liste_effet_avec_equipement(
                liste_arme
            )
            nombre_attaque = caracteristique_avec_equipement.attaque
            liste_attaque = []
            for i in range(0, nombre_attaque):
                liste_attaque.append(
                    AttaqueCac(
                        caracteristique_avec_equipement,
                        liste_effet_avec_equipement,
                    )
                )
            return liste_attaque
        return []

    def get_figurine_equipee(self, liste_arme: list[Arme]) -> Optional[FigurineEquipee]:
        if not is_liste_arme_valid(liste_arme):
            return None
        liste_attaque = self.get_liste_attaque(liste_arme)
        carac_avec_equipement = self.get_caracteristique_avec_equipement(liste_arme)
        liste_effet_avec_equipement = self.get_liste_effet_avec_equipement(liste_arme)
        return FigurineEquipee(
            self.nom,
            self.caracteristique_de_base,
            carac_avec_equipement,
            liste_attaque,
            liste_effet_avec_equipement,
            self.socle,
        )


class FigurineEquipee:
    def __init__(
        self,
        nom: str,
        caracteristique_de_base: Caracteristique,
        caracteristique_effective: Caracteristique,
        liste_attaque: list[AttaqueCac],
        liste_effet: list[Effet],
        socle: Socle,
    ):
        self.nom = nom
        self.caracteristique_de_base = caracteristique_de_base
        self.caracteristique_effective = caracteristique_effective
        self.liste_attaque = liste_attaque
        self.liste_effet = liste_effet
        self.socle = socle


@dataclass
class Fantassin(Figurine):
    def avec_equipement(self, liste_arme: list[Arme]) -> Optional[FigurineEquipee]:
        if is_liste_arme_valid(liste_arme):
            caracteristique_avec_equipement = self.get_caracteristique_avec_equipement(
                liste_arme
            )
            liste_effet_avec_equipement = self.get_liste_effet_avec_equipement(
                liste_arme
            )
            nombre_attaque = caracteristique_avec_equipement.attaque
            liste_attaque = []
            for i in range(0, nombre_attaque):
                liste_attaque.append(
                    AttaqueCac(
                        caracteristique_avec_equipement,
                        liste_effet_avec_equipement,
                    )
                )
            return FigurineEquipee(
                self.nom,
                self.caracteristique_de_base,
                self.get_caracteristique_avec_equipement(liste_arme),
                liste_attaque,
                self.get_liste_effet_avec_equipement(liste_arme),
                self.socle,
            )
        return None


class Champion(Fantassin):
    pass
