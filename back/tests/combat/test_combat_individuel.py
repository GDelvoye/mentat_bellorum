import pytest

from back.src.combat.combat_individuel import (
    jet_de_sauvegarde,
    jet_pour_blesser,
    jet_pour_toucher_cac,
)

testdata_jet_pour_toucher_cac = [
    (3, 3, 4),
    (5, 2, 3),
    (4, 7, 4),
    (4, 8, 5),
]


@pytest.mark.parametrize("cc_att, cc_def, expected", testdata_jet_pour_toucher_cac)
def test_jet_toucher(cc_att: int, cc_def: int, expected: int):
    result = jet_pour_toucher_cac(cc_att, cc_def)
    assert result == expected


testdata_jet_pour_blesser = [
    (2, 5, 6),
    (3, 5, 6),
    (4, 5, 5),
    (5, 5, 4),
    (6, 5, 3),
    (7, 5, 2),
]


@pytest.mark.parametrize("f_att, e_def, expected", testdata_jet_pour_blesser)
def test_jet_blesser_possible(f_att: int, e_def: int, expected: int):
    result = jet_pour_blesser(f_att, e_def)
    assert result == expected


def test_jet_blesser_impossible():
    # Given
    f_att = 1
    e_def = 5
    # When
    result = jet_pour_blesser(f_att, e_def)
    # Then
    assert result is None


testdata_jet_de_sauvegarde = [
    (3, 5, 0, 5),
    (4, 5, 0, 6),
    (3, 5, 1, 6),
    (4, 5, 1, 7),
    (10, 1, 10, 7),
]


@pytest.mark.parametrize(
    "f_att, svg_def, malus_svg, expected", testdata_jet_de_sauvegarde
)
def test_jet_de_sauvegarde(f_att: int, svg_def: int, malus_svg: int, expected: int):
    result = jet_de_sauvegarde(f_att, svg_def, malus_svg)
    assert result == expected
