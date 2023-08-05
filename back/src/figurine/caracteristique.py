from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Caracteristique:
    """Basic carac."""

    mouvement: int = 0
    capa_combat: int = 0
    capa_tir: int = 0
    force: int = 0
    endurance: int = 0
    point_de_vie: int = 0
    initiative: int = 0
    attaque: int = 0
    commandement: int = 0
    sauvegarde: int = 7
    sauvegarde_invulnerable: int = 7

    def __add__(self, carac: Caracteristique) -> Caracteristique:
        return Caracteristique(
            addition_caracteristique(self.mouvement, carac.mouvement, 0, 48),
            addition_caracteristique(self.capa_combat, carac.capa_combat, 0, 10),
            addition_caracteristique(self.capa_tir, carac.capa_tir, 0, 10),
            addition_caracteristique(self.force, carac.force, 0, 10),
            addition_caracteristique(self.endurance, carac.endurance, 0, 10),
            addition_caracteristique(self.point_de_vie, carac.point_de_vie, 0, 10),
            addition_caracteristique(self.initiative, carac.initiative, 0, 10),
            addition_caracteristique(self.attaque, carac.attaque, 0, 10),
            addition_caracteristique(self.commandement, carac.commandement, 0, 12),
            addition_de_sauvegarde(self.sauvegarde, carac.sauvegarde),
            min(self.sauvegarde_invulnerable, carac.sauvegarde_invulnerable),
        )

    def __repr__(self):
        repr = " M|CC|CT| F| E|PV| I| A|Cd|Sv|Si\n"
        repr += f" {self.mouvement}| {self.capa_combat}| {self.capa_tir}| {self.force}| {self.endurance}| {self.point_de_vie}| {self.initiative}| {self.attaque}| {self.commandement}| {self.sauvegarde}| {self.sauvegarde_invulnerable}"
        return repr


def addition_caracteristique(
    carac1: int, carac2: int, minimum: int, maximum: int
) -> int:
    return min(maximum, max(carac1 + carac2, minimum))


def addition_de_sauvegarde(svg1: int, svg2: int) -> int:
    def svg_pure(svg: int) -> int:
        if svg > 0:
            return 7 - svg
        return svg

    pure_svg1 = svg_pure(svg1)
    pure_svg2 = svg_pure(svg2)
    return max(1, min(7, 7 - (pure_svg1 + pure_svg2)))
