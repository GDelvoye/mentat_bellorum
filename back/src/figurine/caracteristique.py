from dataclasses import dataclass


@dataclass
class Caracteristique:
    """Basic carac."""

    mouvement: int
    capa_combat: int
    capa_tir: int
    force: int
    endurance: int
    point_de_vie: int
    initiative: int
    attaque: int
    commandement: int

    def ajout(self, caracteristique):
        return Caracteristique(
            self.mouvement + caracteristique.mouvement,
            self.capa_combat + caracteristique.capa_combat,
            self.capa_tir + caracteristique.capa_tir,
            self.force + caracteristique.force,
            self.endurance + caracteristique.endurance,
            self.point_de_vie + caracteristique.point_de_vie,
            self.initiative + caracteristique.initiative,
            self.attaque + caracteristique.attaque,
            self.commandement + caracteristique.commandement,
        )
