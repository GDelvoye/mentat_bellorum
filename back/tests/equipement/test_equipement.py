import pytest

from back.src.equipement.equipement import Arme, TypeArme, is_liste_arme_valid
from back.src.figurine.caracteristique import Caracteristique

caracteristique = Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

testdata = [
    (
        [
            Arme("", caracteristique, [], [], TypeArme.arme_base),
            Arme("", caracteristique, [], [], TypeArme.arme_base),
        ],
        True,
    ),
    (
        [
            Arme("", caracteristique, [], [], TypeArme.arme_une_main),
            Arme("", caracteristique, [], [], TypeArme.bouclier),
        ],
        True,
    ),
    (
        [
            Arme("", caracteristique, [], [], TypeArme.arme_deux_mains),
            Arme("", caracteristique, [], [], TypeArme.arme_base),
        ],
        False,
    ),
    (
        [
            Arme("", caracteristique, [], [], TypeArme.arme_base),
            Arme("", caracteristique, [], [], TypeArme.arme_base),
            Arme("", caracteristique, [], [], TypeArme.arme_base),
        ],
        False,
    ),
    (
        [],
        False,
    ),
    (
        [
            Arme("", caracteristique, [], [], TypeArme.bouclier),
        ],
        False,
    ),
    (
        [
            Arme("", caracteristique, [], [], TypeArme.arme_deux_mains),
        ],
        True,
    ),
]


@pytest.mark.parametrize("liste_arme, bool_expected", testdata)
def test_is_liste_arme_valid(
    liste_arme: list[Arme],
    bool_expected: bool,
):
    result = is_liste_arme_valid(liste_arme)
    assert result == bool_expected
