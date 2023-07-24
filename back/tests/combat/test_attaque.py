from back.src.combat.attaque import AttaqueCac
from back.src.combat.defense import Defense
from back.src.figurine.caracteristique import Caracteristique


def test_probabilite_toucher():
    # Given
    attaque = AttaqueCac(
        Caracteristique(0, 5, 0, 0, 0, 0, 0, 0, 0, 7, 7),
        [],
    )
    defense = Defense(
        Caracteristique(0, 3, 0, 0, 0, 0, 0, 0, 0, 7, 7),
        [],
    )
    # When
    result = attaque.probabilite_toucher(defense)
    # Then
    assert result == 2
