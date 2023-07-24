from numpy import isclose

from back.src.equipement.arme.arme import Arme
from back.src.equipement.armure.armure import Armure
from back.src.figurine.caracteristique import Caracteristique
from back.src.figurine.figurine import Fantassin, Socle


def test_fantassin():
    # Given
    caracteristique_fantassin = Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7)
    liste_arme = [
        Arme(
            "arme",
            Caracteristique(0, 1, 0, 2, 0, 1, 0, 3, 0, 7, 7),
            [],
        )
    ]
    liste_effet = []
    socle = Socle(30, 45.6)
    armure = Armure(
        "armure",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6),
        [],
    )
    # When
    fantassin = Fantassin(
        "fantassin",
        caracteristique_fantassin,
        liste_arme,
        armure,
        liste_effet,
        socle,
    )
    # Then
    isclose(fantassin.socle.largeur, socle.largeur)
    assert fantassin.liste_arme[0].nom == "arme"
    assert fantassin.caracteristique_de_base.commandement == 7


def test_liste_attaque_fantassin():
    # Given
    caracteristique_fantassin = Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7)
    liste_arme = [
        Arme(
            "deux arme de base",
            Caracteristique(0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 7),
            [],
        ),
        Arme(
            "arme à deux mains",
            Caracteristique(0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 7),
            ["attaque en dernier"],
        ),
    ]
    armure = Armure(
        "armure",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6),
        [],
    )
    liste_effet = []
    socle = Socle(30, 45.6)
    fantassin = Fantassin(
        "fantassin",
        caracteristique_fantassin,
        liste_arme,
        armure,
        liste_effet,
        socle,
    )
    # When
    liste_attaque_base = fantassin.liste_attaque([fantassin.liste_arme[0]])
    liste_attaque_lourde = fantassin.liste_attaque([fantassin.liste_arme[1]])
    # Then
    assert liste_attaque_base[0].caracteristique.force == 3
    assert liste_attaque_base[0].caracteristique.capa_combat == 3
    assert liste_attaque_base[0].caracteristique.attaque == 2
    assert len(liste_attaque_base) == 2
    assert len(liste_attaque_base[0].list_effet) == 0
    assert liste_attaque_lourde[0].caracteristique.force == 5
    assert liste_attaque_lourde[0].caracteristique.capa_combat == 3
    assert liste_attaque_lourde[0].caracteristique.attaque == 1
    assert len(liste_attaque_lourde) == 1
    assert liste_attaque_lourde[0].list_effet[0] == "attaque en dernier"
