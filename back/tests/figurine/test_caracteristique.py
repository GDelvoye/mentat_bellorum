from back.src.figurine.caracteristique import Caracteristique


def test_caracteristique():
    # Given
    caracteristique1 = Caracteristique(1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 4)
    caracteristique2 = Caracteristique(3, 0, 0, 1, 0, 0, 0, 0, 0, 6, 3)
    # When
    caracteristique3 = caracteristique1 + caracteristique2
    # Then
    assert caracteristique3.mouvement == 4
    assert caracteristique3.sauvegarde == 5
    assert caracteristique3.sauvegarde_invulnerable == 3
