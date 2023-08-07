import pytest
from numpy import isclose

from back.src.combat.attaque import AttaqueCac
from back.src.combat.combat_individuel import (
    dict_nb_pv_perdu_probabilite, dict_probabilite_coup_fatal,
    jet_de_sauvegarde, jet_pour_blesser, jet_pour_toucher_cac,
    probabilite_de_blesser, probabilite_de_rater_sa_sauvegarde,
    probabilite_de_toucher_cac,
    probabilite_une_attaque_fait_perdre_un_point_de_vie)
from back.src.figurine.caracteristique import Caracteristique

testdata_jet_pour_toucher_cac = [
    (3, 3, 4),
    (5, 2, 3),
    (4, 7, 4),
    (4, 8, 5),
    (4, 5, 4),
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


testdata_proba_toucher_cac = [
    (3, 3, 1 / 2),
    (4, 3, 2 / 3),
    (4, 5, 1 / 2),
    (4, 8, 1 / 3),
]


@pytest.mark.parametrize("cc_att, cc_def, expected", testdata_proba_toucher_cac)
def test_probabilite_de_toucher_cac(
    cc_att: int,
    cc_def: int,
    expected: float,
):
    result = probabilite_de_toucher_cac(cc_att, cc_def)
    assert isclose(result, expected)


testdata_proba_blesser = [
    (1, 5, 0),
    (2, 5, 1 / 6),
    (3, 5, 1 / 6),
    (4, 5, 1 / 3),
    (5, 5, 1 / 2),
    (6, 5, 2 / 3),
    (7, 5, 5 / 6),
]


@pytest.mark.parametrize("f_att, e_def, expected", testdata_proba_blesser)
def test_probabilite_de_blesser(
    f_att: int,
    e_def: int,
    expected: float,
):
    result = probabilite_de_blesser(f_att, e_def)
    assert isclose(result, expected)


testdata_proba_sauvegarde = [
    (3, 5, 0, 2 / 3),
    (4, 5, 0, 5 / 6),
    (3, 5, 1, 5 / 6),
    (4, 5, 1, 1),
    (10, 1, 10, 1),
]


@pytest.mark.parametrize(
    "f_att, svg_def, malus_svg, expected", testdata_proba_sauvegarde
)
def test_probabilite_de_rater_sa_sauvegarde(
    f_att: int,
    svg_def: int,
    malus_svg: int,
    expected: float,
):
    result = probabilite_de_rater_sa_sauvegarde(f_att, svg_def, malus_svg)
    assert isclose(result, expected)


def test_probabilite_une_attaque_fait_perdre_un_point_de_vie():
    # Given
    attaque = AttaqueCac(
        Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7),
        [],
    )
    carac_defenseur = Caracteristique(4, 4, 4, 4, 4, 2, 4, 2, 8, 4, 5)
    # When
    result = probabilite_une_attaque_fait_perdre_un_point_de_vie(
        attaque,
        carac_defenseur,
    )
    # Then
    assert isclose(result, 1 / 18)


def test_dict_nb_pv_perdu_probabilite():
    # Given
    attaque = AttaqueCac(
        Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7),
        [],
    )
    carac_defenseur = Caracteristique(4, 4, 4, 4, 4, 2, 4, 2, 8, 4, 5)
    # When
    result = dict_nb_pv_perdu_probabilite(
        attaque,
        carac_defenseur,
        ["attaque_empoisonnee"],
        [],
    )
    # Then
    assert isclose(result[1], 1 / 27 + 1 / 18)


def test_dict_probabilite_coup_fatal():
    # Given
    attaque = AttaqueCac(
        Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7),
        [],
    )
    carac_defenseur = Caracteristique(4, 4, 4, 4, 4, 2, 4, 2, 8, 4, 5)
    # When
    result = dict_probabilite_coup_fatal(
        attaque,
        carac_defenseur,
    )
    # Then
    assert isclose(result[1], 1 / 36)
    assert isclose(result[2], 1 / 18)


def test_dict_probabilite_coup_fatal_force_faible_endu_forte():
    # Given
    attaque = AttaqueCac(
        Caracteristique(4, 3, 3, 1, 3, 1, 3, 1, 7, 7, 7),
        [],
    )
    carac_defenseur = Caracteristique(4, 4, 4, 4, 10, 2, 4, 2, 8, 4, 5)
    # When
    result = dict_probabilite_coup_fatal(
        attaque,
        carac_defenseur,
    )
    # Then
    assert isclose(result[1], 0)
    assert isclose(result[2], 1 / 18)
