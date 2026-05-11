"""Classe pour gérer la trajectoire des boules."""

from math import sqrt, atan2, degrees
from boule import Boule


class Trajectoire:
    """
    Gère la trajectoire d'une boule.
    Permet de calculer et prédire les positions futures d'une boule.

    Attributs:
        boule (Boule): La boule dont on suit la trajectoire
        positions_historique (List): Historique des positions
        enregistrer_historique (bool): Si True, enregistre les positions
    """

    def __init__(self, boule: Boule, enregistrer_historique=False):
        """
        Initialise une trajectoire pour une boule.

        Args:
            boule (Boule): La boule à suivre
            enregistrer_historique (bool): Si True, enregistre les positions (par défaut False)
        """
        self.boule = boule
        self.positions_historique = []
        self.enregistrer_historique = enregistrer_historique

        if self.enregistrer_historique:
            self.positions_historique.append((boule.x, boule.y))

    def enregistrer_position(self):
        """Enregistre la position actuelle de la boule dans l'historique."""
        if self.enregistrer_historique:
            self.positions_historique.append((self.boule.x, self.boule.y))

    def obtenir_angle_actuel(self) -> float:
        """
        Calcule l'angle de la trajectoire actuelle.

        Returns:
            float: Angle en degrés (0 = droite, 90 = haut)
        """
        if self.boule.vx == 0 and self.boule.vy == 0:
            return 0

        angle_radians = atan2(self.boule.vy, self.boule.vx)
        return degrees(angle_radians)

    def obtenir_vitesse_actuelle(self) -> float:
        """
        Calcule la vitesse actuelle de la boule.

        Returns:
            float: Norme de la vitesse (distance par unité de temps)
        """
        return sqrt(self.boule.vx ** 2 + self.boule.vy ** 2)

    def predire_position(self, temps: float, coefficient_resistance=0.99) -> tuple:
        """
        Prédit la position future de la boule sans obstacles.
        Approximation linéaire avec application de résistance.

        Args:
            temps (float): Temps pour lequel prédire (en secondes)
            coefficient_resistance (float): Coefficient de résistance (par défaut 0.99)

        Returns:
            tuple: (x_future, y_future)
        """
        x = self.boule.x
        y = self.boule.y
        vx = self.boule.vx
        vy = self.boule.vy

        # Simuler le mouvement avec résistance
        dt = 0.016  # ~60 FPS
        steps = int(temps / dt)

        for _ in range(steps):
            x += vx * dt
            y += vy * dt
            vx *= coefficient_resistance
            vy *= coefficient_resistance

            # Arrêter si la vitesse est presque nulle
            if sqrt(vx ** 2 + vy ** 2) < 0.1:
                break

        return (x, y)

    def predire_distance_parcourue(self, coefficient_resistance=0.99) -> float:
        """
        Prédit la distance totale que parcourra la boule avant de s'arrêter.

        Args:
            coefficient_resistance (float): Coefficient de résistance

        Returns:
            float: Distance estimée
        """
        vx = self.boule.vx
        vy = self.boule.vy
        vitesse_initiale = sqrt(vx ** 2 + vy ** 2)

        if vitesse_initiale == 0:
            return 0

        # Avec résistance, vitesse(t) = vitesse_initiale * r^t
        # Distance total = vitesse_initiale * (1 / ln(1/r)) * (1 - r^t_final)
        # où r = coefficient_resistance
        # Pour simplifier, on utilise une approximation:
        # Distance ≈ vitesse_initiale / (1 - coefficient_resistance)

        if coefficient_resistance >= 1:
            return float('inf')  # Pas de résistance

        distance_estimee = vitesse_initiale / (1 - coefficient_resistance)
        return distance_estimee

    def obtenir_historique(self) -> list:
        """
        Retourne l'historique des positions enregistrées.

        Returns:
            list: Liste des tuples (x, y) de positions enregistrées
        """
        return self.positions_historique.copy()

    def effacer_historique(self):
        """Efface l'historique des positions."""
        self.positions_historique = []

    def __repr__(self):
        """Représentation textuelle de la trajectoire."""
        vitesse = self.obtenir_vitesse_actuelle()
        angle = self.obtenir_angle_actuel()
        return f"Trajectoire(vitesse={vitesse:.2f}, angle={angle:.1f}°, positions_enregistrees={len(self.positions_historique)})"

