"""Classe représentant une boule du jeu BounceBox."""

from enum import Enum
from math import sqrt


class CouleurBoule(Enum):
    """Énumération des couleurs possibles d'une boule."""
    BLANCHE = "blanche"
    GRISE = "grise"
    ROUGE = "rouge"
    BLEUE = "bleue"


class Boule:
    """
    Représente une boule du jeu BounceBox.

    Attributs:
        x (float): Position x de la boule
        y (float): Position y de la boule
        vx (float): Vitesse en x
        vy (float): Vitesse en y
        rayon (float): Rayon de la boule
        couleur (CouleurBoule): Couleur de la boule
        masse (float): Masse de la boule (par défaut 1.0)
    """

    def __init__(self, x, y, couleur, rayon=10, vx=0, vy=0, masse=1.0):
        """
        Initialise une boule.

        Args:
            x (float): Position initiale x
            y (float): Position initiale y
            couleur (CouleurBoule): Couleur de la boule
            rayon (float): Rayon de la boule (par défaut 10)
            vx (float): Vitesse initiale en x (par défaut 0)
            vy (float): Vitesse initiale en y (par défaut 0)
            masse (float): Masse de la boule (par défaut 1.0)
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rayon = rayon
        self.couleur = couleur
        self.masse = masse

    def deplacer(self, dt):
        """
        Déplace la boule selon sa vitesse pendant un intervalle de temps.

        Args:
            dt (float): Intervalle de temps
        """
        self.x += self.vx * dt
        self.y += self.vy * dt

    def appliquer_resistance(self, coefficient_resistance):
        """
        Applique une résistance (frottement) à la boule.

        Args:
            coefficient_resistance (float): Coefficient de résistance (entre 0 et 1)
        """
        self.vx *= coefficient_resistance
        self.vy *= coefficient_resistance

    def arreter(self):
        """Arrête complètement la boule."""
        self.vx = 0
        self.vy = 0

    def est_arrêtee(self, seuil=0.1):
        """
        Vérifie si la boule s'est arrêtée (vitesse très faible).

        Args:
            seuil (float): Seuil de vitesse considéré comme arrêtée

        Returns:
            bool: True si la boule est arrêtée
        """
        vitesse = sqrt(self.vx ** 2 + self.vy ** 2)
        return vitesse < seuil

    def changer_couleur(self, nouvelle_couleur):
        """
        Change la couleur de la boule.

        Args:
            nouvelle_couleur (CouleurBoule): Nouvelle couleur
        """
        self.couleur = nouvelle_couleur

    def distance_vers(self, autre_boule):
        """
        Calcule la distance entre cette boule et une autre.

        Args:
            autre_boule (Boule): L'autre boule

        Returns:
            float: Distance entre les centres des deux boules
        """
        dx = self.x - autre_boule.x
        dy = self.y - autre_boule.y
        return sqrt(dx ** 2 + dy ** 2)

    def entre_en_collision_avec(self, autre_boule):
        """
        Vérifie si cette boule entre en collision avec une autre.

        Args:
            autre_boule (Boule): L'autre boule

        Returns:
            bool: True si les boules se touchent
        """
        distance = self.distance_vers(autre_boule)
        return distance <= (self.rayon + autre_boule.rayon)

    def __repr__(self):
        """Représentation textuelle de la boule."""
        return f"Boule({self.couleur.value}, x={self.x:.1f}, y={self.y:.1f}, vx={self.vx:.1f}, vy={self.vy:.1f})"


class Boule_blanche(Boule):
    """
    Représente la boule blanche du jeu BounceBox.

    La boule blanche est toujours blanche et est utilisée pour frapper
    les autres boules. Elle hérite de Boule.
    """

    def __init__(self, x, y, rayon=10, vx=0, vy=0, masse=1.0):
        """
        Initialise la boule blanche.

        Args:
            x (float): Position initiale x
            y (float): Position initiale y
            rayon (float): Rayon de la boule (par défaut 10)
            vx (float): Vitesse initiale en x (par défaut 0)
            vy (float): Vitesse initiale en y (par défaut 0)
            masse (float): Masse de la boule (par défaut 1.0)
        """
        super().__init__(x, y, CouleurBoule.BLANCHE, rayon, vx, vy, masse)

    def __repr__(self):
        """Représentation textuelle de la boule blanche."""
        return f"Boule_blanche(x={self.x:.1f}, y={self.y:.1f}, vx={self.vx:.1f}, vy={self.vy:.1f})"


class Boule_de_couleur(Boule):
    """
    Représente une boule colorée du jeu BounceBox.

    Les boules de couleur sont de couleur rouge, grise, bleue, etc.
    Elles héritent de Boule.
    """

    def __init__(self, x, y, couleur, rayon=10, vx=0, vy=0, masse=1.0):
        """
        Initialise une boule colorée.

        Args:
            x (float): Position initiale x
            y (float): Position initiale y
            couleur (CouleurBoule): Couleur de la boule (ne doit pas être BLANCHE)
            rayon (float): Rayon de la boule (par défaut 10)
            vx (float): Vitesse initiale en x (par défaut 0)
            vy (float): Vitesse initiale en y (par défaut 0)
            masse (float): Masse de la boule (par défaut 1.0)

        Raises:
            ValueError: Si la couleur est BLANCHE
        """
        if couleur == CouleurBoule.BLANCHE:
            raise ValueError("Une boule colorée ne peut pas être blanche. Utilisez Boule_blanche à la place.")
        super().__init__(x, y, couleur, rayon, vx, vy, masse)

    def __repr__(self):
        """Représentation textuelle de la boule colorée."""
        return f"Boule_de_couleur({self.couleur.value}, x={self.x:.1f}, y={self.y:.1f}, vx={self.vx:.1f}, vy={self.vy:.1f})"


