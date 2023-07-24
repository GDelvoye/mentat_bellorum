from dataclasses import dataclass
from back.figurine.caracteristique import Caracteristique
from back.effet.effet import Effet


@dataclass
class Arme:
    nom: str
    modification_caracteristique: Caracteristique
    liste_effet: list[Effet]
