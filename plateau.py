"""Classe représentant le plateau de jeu BounceBox."""

from typing import List
from boule import Boule, CouleurBoule


class Plateau:
    """
    Représente le plateau de jeu BounceBox.

    Attributs:
        largeur (float): Largeur du plateau
        hauteur (float): Hauteur du plateau
        boules (List[Boule]): Liste des boules sur le plateau
        coefficient_resistance (float): Coefficient de résistance appliqué lors des collisions
        coefficient_bounce (float): Coefficient d'élasticité des rebonds sur les bordures
    """

    def __init__(self, largeur=800, hauteur=600, coefficient_resistance=0.99, coefficient_bounce=0.95):
        """
        Initialise le plateau.

        Args:
            largeur (float): Largeur du plateau (par défaut 800)
            hauteur (float): Hauteur du plateau (par défaut 600)
            coefficient_resistance (float): Coefficient de résistance (par défaut 0.99)
            coefficient_bounce (float): Coefficient d'élasticité (par défaut 0.95)
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.boules: List[Boule] = []
        self.coefficient_resistance = coefficient_resistance
        self.coefficient_bounce = coefficient_bounce

        # Marges pour les rebonds (correspondent aux bordures visuelles)
        self.marge_rebond = 22  # 7 (position) + 15 (épaisseur bordure)

        # Limites effectives pour les rebonds
        self.limite_gauche = self.marge_rebond
        self.limite_droite = self.largeur - self.marge_rebond
        self.limite_haut = self.marge_rebond
        self.limite_bas = self.hauteur - self.marge_rebond

    def ajouter_boule(self, boule: Boule):
        """
        Ajoute une boule au plateau.

        Args:
            boule (Boule): La boule à ajouter
        """
        self.boules.append(boule)

    def retirer_boule(self, boule: Boule):
        """
        Retire une boule du plateau.

        Args:
            boule (Boule): La boule à retirer
        """
        if boule in self.boules:
            self.boules.remove(boule)

    def obtenir_boules_par_couleur(self, couleur: CouleurBoule) -> List[Boule]:
        """
        Retourne toutes les boules d'une couleur donnée.

        Args:
            couleur (CouleurBoule): La couleur recherchée

        Returns:
            List[Boule]: Liste des boules de cette couleur
        """
        return [boule for boule in self.boules if boule.couleur == couleur]

    def obtenir_boule_blanche(self) -> Boule:
        """
        Retourne la boule blanche.

        Returns:
            Boule: La boule blanche (ou None si elle n'existe pas)
        """
        boules_blanches = self.obtenir_boules_par_couleur(CouleurBoule.BLANCHE)
        return boules_blanches[0] if boules_blanches else None

    def gerer_rebond_bordures(self):
        """
        Gère les rebonds des boules sur les bordures du plateau.
        """
        for boule in self.boules:
            # Rebond sur les bordures horizontales (gauche/droite)
            if boule.x - boule.rayon <= self.limite_gauche:
                boule.x = self.limite_gauche + boule.rayon
                boule.vx = -boule.vx * self.coefficient_bounce
            elif boule.x + boule.rayon >= self.limite_droite:
                boule.x = self.limite_droite - boule.rayon
                boule.vx = -boule.vx * self.coefficient_bounce

            # Rebond sur les bordures verticales (haut/bas)
            if boule.y - boule.rayon <= self.limite_haut:
                boule.y = self.limite_haut + boule.rayon
                boule.vy = -boule.vy * self.coefficient_bounce
            elif boule.y + boule.rayon >= self.limite_bas:
                boule.y = self.limite_bas - boule.rayon
                boule.vy = -boule.vy * self.coefficient_bounce

    def appliquer_resistance_toutes_boules(self):
        """
        Applique la résistance à toutes les boules du plateau.
        """
        for boule in self.boules:
            boule.appliquer_resistance(self.coefficient_resistance)

    def mettre_a_jour(self, dt):
        """
        Met à jour le plateau : déplace les boules et gère les rebonds.

        Args:
            dt (float): Intervalle de temps
        """
        # Déplacer toutes les boules
        for boule in self.boules:
            boule.deplacer(dt)

        # Gérer les rebonds sur les bordures
        self.gerer_rebond_bordures()

        # Appliquer la résistance
        self.appliquer_resistance_toutes_boules()

        # Arrêter les boules qui se sont quasiment arrêtées
        for boule in self.boules:
            if boule.est_arrêtee():
                boule.arreter()

    def __repr__(self):
        """Représentation textuelle du plateau."""
        return f"Plateau({self.largeur}x{self.hauteur}, {len(self.boules)} boules)"
