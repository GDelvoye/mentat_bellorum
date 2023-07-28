from back.src.effet.effet import Effet
from back.src.figurine.caracteristique import Caracteristique


def test_is_effet_valide_suppresseur_false():
    # Given
    effet = Effet(
        "regeneration",
        Caracteristique(sauvegarde_invulnerable=4),
        Caracteristique(),
        [],
        [],
        [],
        ["attaque_enflammee"],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee"]
    liste_effet_adverse = ["charge", "peur", "attaque_enflammee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert not result


def test_is_effet_valide_suppresseur_true():
    # Given
    effet = Effet(
        "regeneration",
        Caracteristique(sauvegarde_invulnerable=4),
        Caracteristique(),
        [],
        [],
        [],
        ["attaque_enflammee"],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee"]
    liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert result


def test_is_effet_valide_necessaire_false():
    # Given
    effet = Effet(
        "horde",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["charge"],
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
    effet = Effet(
        "horde",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["charge"],
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
    effet = Effet(
        "attaque_sur_deux_rangs_lance",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4),
        Caracteristique(),
        ["position_rang_2"],
        [],
        ["charge", "de_flanc", "de_dos"],
        ["flanc", "dos"],
    )
    liste_effet_allie = ["tenace", "attaque_enflammee", "position_rang_2"]
    liste_effet_adverse = ["charge", "peur", "attaque_empoisonnee"]
    # When
    result = effet.is_valide(liste_effet_allie, liste_effet_adverse)
    # Then
    assert result
