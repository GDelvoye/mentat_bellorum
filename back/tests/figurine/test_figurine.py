from back.src.effet.effet import Dependances, EffetTheorique
from back.src.equipement.equipement import Arme, Armure, TypeArme
from back.src.figurine.caracteristique import Caracteristique
from back.src.figurine.figurine import Fantassin, Socle

figurine = Fantassin(
    nom="",
    caracteristique_de_base=Caracteristique(4, 3, 3, 3, 3, 1, 3, 1, 7, 7, 7),
    liste_arme=[
        Arme(
            "deux arme de base",
            Caracteristique(0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 7),
            [],
            [],
            TypeArme.arme_deux_mains,
        ),
        Arme(
            "arme à deux mains",
            Caracteristique(force=2),
            [
                EffetTheorique(
                    "attaque en dernier",
                    Caracteristique(),
                    Caracteristique(),
                    Dependances(
                        set(),
                        set(),
                        set(),
                        set(),
                        set(),
                    )
                )
            ],
            [],
            TypeArme.arme_deux_mains,
        ),
    ],
    armure=Armure(
        "armure",
        Caracteristique(0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6),
        [],
    ),
    liste_effet=[],
    socle=Socle(30, 45.6),
)


def test_avec_equipement_valide():
    # Given figurine
    # When
    figurine_equipee = figurine.avec_equipement([figurine.liste_arme[0]])
    # Then
    assert figurine_equipee is not None


def test_avec_equipement_non_valide():
    # Given figurine
    # When
    figurine_equipee = figurine.avec_equipement(figurine.liste_arme)
    # Then
    assert figurine_equipee is None


def test_get_caracteristique_avec_equipement_force():
    # Given figurine
    # When
    carac_avec_equipement = figurine.get_caracteristique_avec_equipement(
        [figurine.liste_arme[1]]
    )
    # Then
    assert carac_avec_equipement.force == 5


def test_get_caracteristique_avec_equipement_sauvegarde():
    # Given figurine
    # When
    carac_avec_equipement = figurine.get_caracteristique_avec_equipement(
        [figurine.liste_arme[1]]
    )
    # Then
    assert carac_avec_equipement.sauvegarde == 5


def test_get_caracteristique_avec_equipement_sauvegarde_invulnerable():
    # Given figurine
    # When
    carac_avec_equipement = figurine.get_caracteristique_avec_equipement(
        [figurine.liste_arme[1]]
    )
    # Then
    assert carac_avec_equipement.sauvegarde_invulnerable == 6


def test_get_liste_effet_avec_equipement():
    # Given figurine
    # When
    liste_effet_avec_equipement = figurine.get_liste_effet_avec_equipement(
        [figurine.liste_arme[1]]
    )
    # Then
    assert liste_effet_avec_equipement[0].nom == "attaque en dernier"


def test_figurine_equipee_liste_attaque():
    # Given figurine
    figurine_equipee = figurine.avec_equipement([figurine.liste_arme[1]])
    # When
    liste_attaque = figurine_equipee.liste_attaque
    # Then
    assert len(liste_attaque) == 1
