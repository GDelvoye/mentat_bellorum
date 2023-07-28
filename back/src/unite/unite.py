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
