import os

import pandas as pd

from back.src.effet.effet import Dependances, EffetTheorique
from back.src.figurine.caracteristique import Caracteristique
from back.src.parser.dict_effet_from_csv import dict_effet

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
        return int(df_nom[nom_colonne].values[0])


# def convert_effet_to_typearme(liste_effet: list[Effet]) -> TypeArme:
#     if EnumEffet.arme_a_deux_mains.value in liste_effet:
#         return TypeArme.arme_deux_mains
#     else:
#         return TypeArme.arme_base  # Faux, a modifier


def get_liste_effet_from_liste_nom(liste_nom: list[str]) -> list[str]:
    liste_effet = []
    for nom in liste_nom:
        liste_effet.append(dict_effet[nom])
    return liste_effet


# def create_arme_ori(nom_arme: str):
#     if nom_arme in df_arme["nom"].values:
#         liste_nom_effet_associe = recover_set_from_cell(nom_arme, "effet")
#         liste_nom_necessaire_allie = recover_set_from_cell(nom_arme, "necessaire_allie")
#         bonus_force = recover_value_from_cell(nom_arme, "bonus_force")
#         bonus_att = recover_value_from_cell(nom_arme, "bonus_att")
#         return Arme(
#             nom_arme,
#             Caracteristique(force=bonus_force, attaque=bonus_att),
#             get_liste_effet_from_liste_nom(liste_nom_effet_associe),
#             get_liste_effet_from_liste_nom(liste_nom_necessaire_allie),
#             convert_effet_to_typearme(liste_nom_effet_associe),
#         )
#     else:
#         print(f"{nom_arme} pas dans csv")


def create_arme(nom_arme: str):
    if nom_arme in df_arme["nom"].values:
        liste_nom_effet_associe = recover_set_from_cell(nom_arme, "effet")
        liste_nom_necessaire_allie = recover_set_from_cell(nom_arme, "necessaire_allie")
        bonus_force = recover_value_from_cell(nom_arme, "bonus_force")
        bonus_att = recover_value_from_cell(nom_arme, "bonus_att")
        return EffetTheorique(
            nom_arme,
            Caracteristique(force=bonus_force, attaque=bonus_att),
            Caracteristique(),
            Dependances(
                liste_nom_necessaire_allie,
                set(),
                set(),
                set(),
                liste_nom_effet_associe,
            )
        )
    else:
        print(f"{nom_arme} pas dans csv")


def create_dict_arme() -> dict[str, EffetTheorique]:
    dict = {}
    for n in df_arme["nom"].values:
        dict[n] = create_arme(n)
    return dict


dict_arme = create_dict_arme()
