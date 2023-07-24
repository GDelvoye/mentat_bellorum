from dataclasses import dataclass
from back.src.figurine.caracteristique import Caracteristique
from back.src.effet.effet import Effet


@dataclass
class Arme:
    nom: str
    modification_caracteristique: Caracteristique
    liste_effet: list[Effet]
