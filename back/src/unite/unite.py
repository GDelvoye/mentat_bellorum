from dataclasses import dataclass

from back.src.figurine.figurine import Figurine


@dataclass
class Unite:
    dict_figurine_nombre: dict[Figurine, int]
    liste_effet: list

    def assigne_positions_dans_unite(self):
        """
        Assigne à chaque figurine une position en terme de rang et de colonne.
        """
        pass

    def reorganisation(self, taille_du_front: int):
        """
        Change la taile du front de l'unité.
        """
        pass

    def ajout_figurine(self, figurine):
        pass

    def suppression_figurine(self):
        pass

    def ajout_effet(self):
        pass

    def declaration_de_charge(self, unite_adverse):
        # return UniteCombat(copy.self, copy.unite_adverse)
        pass


def declaration_de_charge(unite_1, unite_2):
    # return UniteCombat()
    pass


@dataclass
class UniteCombat:
    liste_unite: list  # ou alors

    round: int
    liste_effet: list

    def resultat_round(self):
        pass

    def round_suivant(self):
        pass
