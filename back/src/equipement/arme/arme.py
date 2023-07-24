from dataclasses import dataclass

from back.src.effet.effet import Effet
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Arme:
    nom: str
    modification_caracteristique: Caracteristique
    liste_effet: list[Effet]
