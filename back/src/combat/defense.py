from dataclasses import dataclass

from back.src.effet.effet import Effet
from back.src.figurine.caracteristique import Caracteristique


@dataclass
class Defense:
    caracteristique: Caracteristique
    list_effet: list[Effet]
