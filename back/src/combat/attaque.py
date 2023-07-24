from abc import ABC, abstractmethod
from dataclasses import dataclass

from back.src.combat.defense import Defense
from back.src.effet.effet import Effet
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Attaque(ABC):
    caracteristique: Caracteristique
    list_effet: list[Effet]

    @abstractmethod
    def probabilite_toucher(self):
        pass

    def probabilite_blesser(self, defense: Defense):
        pass


class AttaqueCac(Attaque):
    def probabilite_toucher(self, defense: Defense):
        return self.caracteristique.capa_combat - defense.caracteristique.capa_combat

    def probabilite_blesser(self, defense: Defense):
        return super().probabilite_blesser(defense)
