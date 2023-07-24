from dataclasses import dataclass
from back.src.figurine.caracteristique import Caracteristique
from back.src.effet.effet import Effet


@dataclass
class Defense:
    caracteristique: Caracteristique
    list_effet: list[Effet]
