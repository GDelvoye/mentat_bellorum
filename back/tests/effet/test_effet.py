import pytest

from back.src.effet.effet import (Dependances, EffetPratique, get_dependances,
                                  get_dict_effet_pratique_from_liste_nom,
                                  get_set_effet_pratique_valide_from_liste_nom)
from back.src.parser.dict_effet_from_csv import dict_effet
from back.src.parser.type import EnumEffet

# def test_is_effet_valide_suppresseur_false():
#     # Given
#     effet = EffetTheorique(
#         "regeneration",
#         Caracteristique(sauvegarde_invulnerable=4),
#         Caracteristique(),
#         [],
#         [],
#         [],
#         ["attaque_enflammee"],
#         [],
#     )
#     liste_effet_allie = ["tenace", "attaque_enflammee"]
#     liste_effet_adverse = ["charge", "peur", "attaque_enflammee"]
#     # When
#     result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
#     # Then
#     assert not result


# def test_is_effet_valide_suppresseur_true():
#     # Given
#     effet = EffetTheorique(
#         "regeneration",
#         Caracteristique(sauvegarde_invulnerable=4),
#         Caracteristique(),
#         [],
#         [],
#         [],
#         ["attaque_enflammee"],
#         [],
#     )
#     liste_effet_allie = ["tenace", "attaque_enflammee"]
#     liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
#     # When
#     result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
#     # Then
#     assert result


# def test_is_effet_valide_necessaire_false():
#     # Given
#     effet = EffetTheorique(
#         "horde",
#         Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
#         Caracteristique(),
#         ["charge"],
#         [],
#         [],
#         [],
#         [],
#     )
#     liste_effet_allie = ["tenace", "attaque_enflammee"]
#     liste_effet_adverse = ["charge"]
#     # When
#     result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
#     # Then
#     assert not result


# def test_is_effet_valide_necessaire_true_allie():
#     # Given
#     effet = EffetTheorique(
#         "horde",
#         Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
#         Caracteristique(),
#         ["charge"],
#         [],
#         [],
#         [],
#         [],
#     )
#     liste_effet_allie = ["tenace", "attaque_enflammee", "charge"]
#     liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
#     # When
#     result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
#     # Then
#     assert result


# def test_is_effet_valide_combat_deux_rangs():
#     # Given
#     effet = EffetTheorique(
#         "attaque_sur_deux_rangs_lance",
#         Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
#         Caracteristique(),
#         ["position_rang_2"],
#         [],
#         ["charge", "de_flanc", "de_dos"],
#         ["flanc", "dos"],
#         [],
#     )
#     liste_effet_allie = ["tenace", "attaque_enflammee", "position_rang_2"]
#     liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
#     # When
#     result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
#     # Then
#     assert result


def test_dependances_get_all():
    # Given
    dependance = Dependances(set("a"), set(), set(["b", "c"]), set(), set())
    # When
    result = dependance.all_dependances()
    # Then
    assert result == set(["c", "b", "a"])


def test_dependance_is_valide_necessaire_allie():
    # Given
    dependance_a_tester = Dependances(set(["a", "b"]), set(), set(), set(), set())
    dependance_de_reference = Dependances(set("a"), set(), set(), set(), set())
    # When
    result = dependance_a_tester.is_valide_necessaire_allie(dependance_de_reference)
    # Then
    assert result is True


def test_dependance_is_valide_suppresseur_allie():
    # Given
    dependance_a_tester = Dependances(set(), set(), set(["a", "b"]), set(), set())
    dependance_de_reference = Dependances(set(), set(), set("a"), set(), set())
    # When
    result = dependance_a_tester.is_valide_suppresseur_allie(dependance_de_reference)
    # Then
    assert result is False


def test_dependance_is_valide():
    # Given
    dependance_a_tester = Dependances(set(["e"]), set(), set(["c", "b"]), set(), set())
    dependance_de_reference = Dependances(set(), set(), set("a"), set(), set())
    # When
    result = dependance_a_tester.is_valide_suppresseur_allie(dependance_de_reference)
    # Then
    assert result is True


def test_get_dict_effet_pratique_from_liste_nom():
    # Given
    liste_nom = [
        EnumEffet.horde.value,
        EnumEffet.charge.value,
    ]
    dict_effet_theorique = dict_effet
    # When
    result = get_dict_effet_pratique_from_liste_nom(
        set_nom=liste_nom,
        dict_effet_theorique=dict_effet_theorique,
    )[EnumEffet.horde.value]
    assert len(result.set_des_effets_pratiques_dependances) == 1


testdata_get_dependances = [
    (
        EnumEffet.charge.value,
        [EnumEffet.charge.value, EnumEffet.premier_tour.value],
        [EnumEffet.premier_tour.value],
    ),
    (
        EnumEffet.charge.value,
        [EnumEffet.charge.value, EnumEffet.premier_tour.value],
        [EnumEffet.premier_tour.value],
    ),
    (
        EnumEffet.premier_tour.value,
        [EnumEffet.deuxieme_tour.value, EnumEffet.premier_tour.value],
        [EnumEffet.deuxieme_tour.value],
    ),
]


@pytest.mark.parametrize(
    "nom, set_de_noms_allies, liste_expected", testdata_get_dependances
)
def test_get_dependances(
    nom: str,
    set_de_noms_allies: list[str],
    liste_expected: list[str],
):
    dict_effet_theorique = dict_effet
    result = get_dependances(
        nom,
        dict_effet_theorique=dict_effet_theorique,
        set_de_noms_allie=set(set_de_noms_allies),
    ).all_dependances()
    assert result == set(liste_expected)


def test_get_dependance_suppresseur_allie():
    # Given
    liste_de_noms_allie = [EnumEffet.deuxieme_tour.value, EnumEffet.premier_tour.value]
    dict_effet_theorique = dict_effet
    # When
    result = get_dependances(
        EnumEffet.premier_tour.value,
        dict_effet_theorique=dict_effet_theorique,
        set_de_noms_allie=liste_de_noms_allie,
    )
    # Then
    assert result.suppresseur_allie == set([EnumEffet.deuxieme_tour.value])


testdata_get_set_effet = [
    (
        [
            EnumEffet.charge.value,
            EnumEffet.premier_tour.value,
        ],
        [
            EnumEffet.charge.value,
            EnumEffet.premier_tour.value,
        ],
    ),
    (
        [
            EnumEffet.horde.value,
            EnumEffet.charge.value,
        ],
        [],
    ),
    (
        [
            EnumEffet.horde.value,
            EnumEffet.charge.value,
            EnumEffet.premier_tour.value,
        ],
        [
            EnumEffet.horde.value,
            EnumEffet.charge.value,
            EnumEffet.premier_tour.value,
        ],
    ),
    (
        [
            EnumEffet.horde.value,
            EnumEffet.premier_tour.value,
            EnumEffet.deuxieme_tour.value,
        ],
        [EnumEffet.deuxieme_tour.value],
    ),
]


@pytest.mark.parametrize(
    "liste_effet_allie, liste_effet_expected", testdata_get_set_effet
)
def test_get_set_effet_pratique_valide_from_liste_nom2(
    liste_effet_allie: list[str],
    liste_effet_expected: list[str],
):
    dict_effet_theorique = dict_effet
    result = get_set_effet_pratique_valide_from_liste_nom(
        liste_effet_allie, dict_effet_theorique
    )
    assert result == set(liste_effet_expected)
