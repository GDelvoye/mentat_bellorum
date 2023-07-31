import os

import pandas as pd

from back.src.effet.effet import Effet
from back.src.equipement.equipement import Arme, TypeArme
from back.src.figurine.caracteristique import Caracteristique
from back.src.parser.type import EnumEffet

csv_file = os.path.join("back", "data", "armes.csv")
df_arme = pd.read_csv(csv_file)


def recover_set_from_cell(nom_arme, nom_colonne):
    df_nom = df_arme[df_arme["nom"] == nom_arme]
    if df_nom.isnull()[nom_colonne].values[0]:
        return set()
    else:
        liste = df_nom[nom_colonne].values[0].split(";")
        if "" in liste:
            liste.remove("")
        return set(liste)


def recover_value_from_cell(nom_arme, nom_colonne):
    df_nom = df_arme[df_arme["nom"] == nom_arme]
    if df_nom.isnull()[nom_colonne].values[0]:
        return 0
    else:
        return df_nom[nom_colonne].values[0]


def convert_effet_to_typearme(liste_effet: list[Effet]) -> TypeArme:
    if EnumEffet.arme_a_deux_mains.value in liste_effet:
        return TypeArme.arme_deux_mains
    else:
        return TypeArme.arme_base  # Faux, a modifier


def create_arme(nom_arme: str):
    if nom_arme in df_arme["nom"].values:
        liste_effet_associe = recover_set_from_cell(nom_arme, "effet")
        liste_necessaire_allie = recover_set_from_cell(nom_arme, "necessaire_allie")
        bonus_force = recover_value_from_cell(nom_arme, "bonus_force")
        bonus_att = recover_value_from_cell(nom_arme, "bonus_att")
        return Arme(
            nom_arme,
            Caracteristique(force=bonus_force, attaque=bonus_att),
            liste_effet_associe,
            liste_necessaire_allie,
            convert_effet_to_typearme(liste_effet_associe),
        )
    else:
        print(f"{nom_arme} pas dans csv")


def create_dict_arme():
    dict = {}
    for n in df_arme["nom"].values:
        dict[n] = create_arme(n)
    return dict


dict_arme = create_dict_arme()
