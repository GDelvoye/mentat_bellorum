import pytest

from back.src.figurine.caracteristique import Caracteristique

testdata = [
    (
        Caracteristique(1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 4),
        Caracteristique(3, 0, 0, 1, 0, 0, 0, 0, 0, 6, 3),
        Caracteristique(4, 0, 0, 1, 0, 0, 0, 0, 0, 5, 3),
    ),
    (
        Caracteristique(1, 0, 0, -1, 0, 0, 0, 0, 0, 6, 4),
        Caracteristique(-3, 0, 0, 1, 0, 0, 0, 0, 13, 1, 1),
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 1),
    ),
    (
        Caracteristique(1, 0, 0, 10, 0, 0, 0, 0, 0, 6, 6),
        Caracteristique(3, 0, 0, 1, 0, 0, 0, 0, 0, -2, 7),
        Caracteristique(4, 0, 0, 10, 0, 0, 0, 0, 0, 7, 6),
    ),
]


@pytest.mark.parametrize("c1, c2, c_expected", testdata)
def test_caracteristique(
    c1: Caracteristique, c2: Caracteristique, c_expected: Caracteristique
):
    result = c1 + c2
    assert result.mouvement == c_expected.mouvement
    assert result.force == c_expected.force
    assert result.commandement == c_expected.commandement
    assert result.sauvegarde == c_expected.sauvegarde
    assert result.sauvegarde_invulnerable == c_expected.sauvegarde_invulnerable
