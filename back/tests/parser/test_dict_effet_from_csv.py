from back.src.effet.effet import EffetTheorique
from back.src.parser.dict_effet_from_csv import dict_effet
from back.src.parser.type import EnumEffet


def test_dict_effet():
    for enum in EnumEffet:
        assert dict_effet[enum.value].nom == enum.value


def test_dict_effet_dependance():
    for enum in EnumEffet:
        effet_theorique: EffetTheorique = dict_effet[enum.value]
        all_dependance = set()
        all_dependance.union(effet_theorique.dependances.effet_inclu)
        all_dependance.union(effet_theorique.dependances.necessaire_adverse)
        all_dependance.union(effet_theorique.dependances.necessaire_allie)
        all_dependance.union(effet_theorique.dependances.suppresseur_adverse)
        all_dependance.union(effet_theorique.dependances.suppresseur_allie)
        for dep_nom in all_dependance:
            assert dep_nom in dict_effet.keys()
