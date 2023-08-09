from typing import Set

import pytest

from back.src.effet.effet import (
    Dependances, get_dependances_from_ensembles_noms_effets,
    get_dict_effet_pratique_avant_ckeck_is_valide,
    get_ensemble_des_effet_pratique_valide_apres_check)
from back.src.parser.type import EnumEffet


def test_dependances_get_all():
    # Given
    dependance = Dependances(set("a"), set(), set(["b", "c"]), set(), set())
    # When
    result = dependance.all_dependances()
    # Then
    assert result == set(["c", "b", "a"])


def test_dependances_is_valide_necessaire_allie():
    # Given
    dependance_a_tester = Dependances(set(["a", "b"]), set(), set(), set(), set())
    dependance_de_reference = Dependances(set("a"), set(), set(), set(), set())
    # When
    result = dependance_a_tester.is_valide_necessaire_allie(dependance_de_reference)
    # Then
    assert result is True


def test_dependances_is_valide_suppresseur_allie():
    # Given
    dependance_a_tester = Dependances(set(), set(), set(["a", "b"]), set(), set())
    dependance_de_reference = Dependances(set(), set(), set("a"), set(), set())
    # When
    result = dependance_a_tester.is_valide_suppresseur_allie(dependance_de_reference)
    # Then
    assert result is False


def test_dependances_is_valide_suppresseur_adverse():
    # Given
    dependance_a_tester = Dependances(set(), set(), set(["a", "b"]), set("c"), set())
    dependance_de_reference = Dependances(set(), set(), set("a"), set("d"), set())
    # When
    result = dependance_a_tester.is_valide_suppresseur_adverse(dependance_de_reference)
    # Then
    assert result is True


testdata_dependances_is_valide_method = [
    (
        Dependances(set(), set(), set(["a", "b"]), set(), set()),
        Dependances(set(), set(), set("a"), set(), set()),
        False,
    ),
    (
        Dependances(set(), set(), set(["a", "b"]), set("c"), set()),
        Dependances(set(), set(), set("a"), set("d"), set()),
        False,
    ),
    (
        Dependances(set(["e"]), set(), set(["c", "b"]), set("e"), set()),
        Dependances(set("e"), set(), set("a"), set("a"), set()),
        True,
    ),
    (
        Dependances(set(["e"]), set(), set(["c", "b"]), set("a"), set()),
        Dependances(set("e"), set(), set("a"), set("a"), set()),
        False,
    ),
]


@pytest.mark.parametrize(
    "dependances_a_tester, dependances_de_reference, expected",
    testdata_dependances_is_valide_method,
)
def test_dependances_is_valide_method(
    dependances_a_tester: Dependances,
    dependances_de_reference: Dependances,
    expected: bool,
):
    result = dependances_a_tester.is_valide(dependances_de_reference)
    assert result is expected


def test_get_dict_effet_pratique_avant_ckeck_is_valide():
    # Given
    noms_effets_allies = set(
        [
            EnumEffet.horde.value,
            EnumEffet.charge.value,
        ]
    )
    # When
    result = get_dict_effet_pratique_avant_ckeck_is_valide(
        noms_effets_allies=noms_effets_allies,
    )[EnumEffet.horde.value]
    assert len(result.effets_pratiques_directements_dependants) == 1


testdata_get_dependances = [
    (
        EnumEffet.charge.value,
        set([EnumEffet.charge.value, EnumEffet.premier_tour.value]),
        set(),
        set([EnumEffet.premier_tour.value]),
    ),
    (
        EnumEffet.charge.value,
        set([EnumEffet.charge.value, EnumEffet.premier_tour.value]),
        set(),
        set([EnumEffet.premier_tour.value]),
    ),
    (
        EnumEffet.premier_tour.value,
        set([EnumEffet.deuxieme_tour.value, EnumEffet.premier_tour.value]),
        set(),
        set([EnumEffet.deuxieme_tour.value]),
    ),
    (EnumEffet.regeneration.value, set(), set(), set()),
    (
        EnumEffet.regeneration.value,
        set(),
        set([EnumEffet.attaque_enflammee.value]),
        set([EnumEffet.attaque_enflammee.value]),
    ),
]


@pytest.mark.parametrize(
    "nom, noms_effets_allies, noms_effets_adverses, noms_effets_expected",
    testdata_get_dependances,
)
def test_get_dependances__from_ensembles_noms_effets_check_all_dependances(
    nom: str,
    noms_effets_allies: Set[str],
    noms_effets_adverses: Set[str],
    noms_effets_expected: Set[str],
):
    result = get_dependances_from_ensembles_noms_effets(
        nom,
        noms_effets_allies=noms_effets_allies,
        noms_effets_adverses=noms_effets_adverses,
    ).all_dependances()
    assert result == noms_effets_expected


def test_get_dependancess_from_ensembles_noms_effets_suppresseur_allie():
    # Given
    noms_effets_allies = set(
        [EnumEffet.deuxieme_tour.value, EnumEffet.premier_tour.value]
    )
    # When
    result = get_dependances_from_ensembles_noms_effets(
        EnumEffet.premier_tour.value,
        noms_effets_allies=noms_effets_allies,
    )
    # Then
    assert result.suppresseur_allie == set([EnumEffet.deuxieme_tour.value])


testdata_get_set_effet = [
    (
        set(
            [
                EnumEffet.charge.value,
                EnumEffet.premier_tour.value,
            ]
        ),
        set(),
        set(
            [
                EnumEffet.charge.value,
                EnumEffet.premier_tour.value,
            ]
        ),
    ),
    (
        set(
            [
                EnumEffet.horde.value,
                EnumEffet.charge.value,
            ]
        ),
        set(),
        set(),
    ),
    (
        set(
            [
                EnumEffet.horde.value,
                EnumEffet.charge.value,
                EnumEffet.premier_tour.value,
            ]
        ),
        set(),
        set(
            [
                EnumEffet.horde.value,
                EnumEffet.charge.value,
                EnumEffet.premier_tour.value,
            ]
        ),
    ),
    (
        set(
            [
                EnumEffet.horde.value,
                EnumEffet.premier_tour.value,
                EnumEffet.deuxieme_tour.value,
            ]
        ),
        set(),
        set([EnumEffet.deuxieme_tour.value]),
    ),
    (
        set(
            [
                EnumEffet.combat_sur_deux_rangs.value,
                EnumEffet.charge.value,
                EnumEffet.premier_tour.value,
                EnumEffet.deuxieme_tour.value,
            ]
        ),
        set(),
        set([EnumEffet.combat_sur_deux_rangs.value, EnumEffet.deuxieme_tour.value]),
    ),
    (
        set([EnumEffet.regeneration.value]),
        set([EnumEffet.attaque_enflammee.value]),
        set(),
    ),
    (
        set([EnumEffet.aura.value]),
        set([EnumEffet.degat_magique.value]),
        set(),
    ),
]


@pytest.mark.parametrize(
    "noms_effets_allies, noms_effets_adverses, noms_effets_expected",
    testdata_get_set_effet,
)
def test_get_ensemble_des_effet_pratique_valide_apres_check(
    noms_effets_allies: Set[str],
    noms_effets_adverses: Set[str],
    noms_effets_expected: Set[str],
):
    result = get_ensemble_des_effet_pratique_valide_apres_check(
        noms_effets_allies,
        noms_effets_adverses,
    )
    assert result == noms_effets_expected
