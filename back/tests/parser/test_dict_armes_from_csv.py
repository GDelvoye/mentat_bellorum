from back.src.effet.effet import Effet
from back.src.equipement.equipement import Arme
from back.src.parser.dict_arme_from_csv import dict_arme
from back.src.parser.dict_effet_from_csv import dict_effet
from back.src.parser.type import EnumArme


def test_dict_arme():
    for enum_arme in EnumArme:
        arme: Arme = dict_arme[enum_arme.value]
        print(arme.nom)
        assert arme.nom == enum_arme.value


def test_dict_arme_dependance():
    for enum in EnumArme:
        arme: Effet = dict_arme[enum.value]
        all_dependance = set()
        all_dependance.union(arme.set_nom_effet_inclu)
        all_dependance.union(arme.set_nom_effet_necessaire_adverse)
        all_dependance.union(arme.set_nom_effet_necessaire_allie)
        all_dependance.union(arme.set_nom_effet_suppresseur_adverse)
        all_dependance.union(arme.set_nom_effet_suppresseur_allie)
        for dep_nom in all_dependance:
            assert dep_nom in (dict_effet.keys() or dict_arme.keys())
