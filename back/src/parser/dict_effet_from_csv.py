import os

import pandas as pd

from back.src.effet.effet import EffetTheorique
from back.src.figurine.caracteristique import Caracteristique

csv_file = os.path.join("back", "data", "effets.csv")
df_effet = pd.read_csv(csv_file)


def recover_set_from_cell(nom_effet, nom_colonne):
    df_nom = df_effet[df_effet["nom"] == nom_effet]
    if df_nom.isnull()[nom_colonne].values[0]:
        return set()
    else:
        liste = df_nom[nom_colonne].values[0].split(";")
        if "" in liste:
            liste.remove("")
        return set(liste)


def create_effet(nom_effet: str):
    if nom_effet in df_effet["nom"].values:
        liste_necessaire_allie = recover_set_from_cell(nom_effet, "necessaire_allie")
        liste_necessaire_adverse = recover_set_from_cell(
            nom_effet, "necessaire_adverse"
        )
        liste_suppresseur_allie = recover_set_from_cell(nom_effet, "suppresseur_allie")
        liste_suppresseur_adverse = recover_set_from_cell(
            nom_effet, "suppresseur_adverse"
        )
        liste_effet_inclu = recover_set_from_cell(nom_effet, "effet_inclu")
        return EffetTheorique(
            nom_effet,
            Caracteristique(),
            Caracteristique(),
            set(liste_necessaire_allie),
            set(liste_necessaire_adverse),
            set(liste_suppresseur_allie),
            set(liste_suppresseur_adverse),
            set(liste_effet_inclu),
        )
    else:
        print(f"{nom_effet} pas dans csv")


def create_dict_effet():
    dict = {}
    for n in df_effet["nom"].values:
        dict[n] = create_effet(n)
    return dict


dict_effet = create_dict_effet()
