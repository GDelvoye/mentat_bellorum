from back.src.effet.effet import EffetTheorique, get_set_effet_pratique_valide_from_liste_nom
from back.src.figurine.caracteristique import Caracteristique
from back.src.parser.dict_effet_from_csv import dict_effet
from back.src.parser.type import EnumEffet


def test_is_effet_valide_suppresseur_false():
    # Given
    effet = EffetTheorique(
        "regeneration",
        Caracteristique(sauvegarde_invulnerable=4),
        Caracteristique(),
        [],
        [],
        [],
        ["attaque_enflammee"],
        [],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee"]
    liste_effet_adverse = ["charge", "peur", "attaque_enflammee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert not result


def test_is_effet_valide_suppresseur_true():
    # Given
    effet = EffetTheorique(
        "regeneration",
        Caracteristique(sauvegarde_invulnerable=4),
        Caracteristique(),
        [],
        [],
        [],
        ["attaque_enflammee"],
        [],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee"]
    liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert result


def test_is_effet_valide_necessaire_false():
    # Given
    effet = EffetTheorique(
        "horde",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["charge"],
        [],
        [],
        [],
        [],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee"]
    liste_effet_adverse = ["charge"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert not result


def test_is_effet_valide_necessaire_true_allie():
    # Given
    effet = EffetTheorique(
        "horde",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["charge"],
        [],
        [],
        [],
        [],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee", "charge"]
    liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert result


def test_is_effet_valide_combat_deux_rangs():
    # Given
    effet = EffetTheorique(
        "attaque_sur_deux_rangs_lance",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["position_rang_2"],
        [],
        ["charge", "de_flanc", "de_dos"],
        ["flanc", "dos"],
        [],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee", "position_rang_2"]
    liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert result


def test_get_set_effet_pratique_valide_from_liste_nom_set_vide():
    # Given
    liste_nom = [
        EnumEffet.horde.value,
        EnumEffet.charge.value,
    ]
    # When
    result = get_set_effet_pratique_valide_from_liste_nom(
        liste_nom=liste_nom,
        dict_effet_theorique=dict_effet,
    )
    # Then
    assert result == set()


def test_get_set_effet_pratique_valide_from_liste_nom_set_valide():
    # Given
    liste_nom = [
        EnumEffet.horde.value,
        EnumEffet.charge.value,
        EnumEffet.premier_tour.value,
    ]
    # When
    result = get_set_effet_pratique_valide_from_liste_nom(
        liste_nom=liste_nom,
        dict_effet_theorique=dict_effet,
    )
    # Then
    assert result.difference(set(liste_nom)) == set()
