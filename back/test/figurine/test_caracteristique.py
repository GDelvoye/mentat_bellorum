from back.src.figurine.caracteristique import Caracteristique


def test_caracteristique():
    # Given
    caracteristique1 = Caracteristique(1, 0, 0, 0, 0, 0, 0, 0, 0)
    caracteristique2 = Caracteristique(3, 0, 0, 1, 0, 0, 0, 0, 0)
    # When
    caracteristique3 = caracteristique1.ajout(caracteristique2)
    # Then
    assert caracteristique3.mouvement == 4
