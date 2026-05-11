"""Classe représentant un joueur du jeu BounceBox."""

from boule import CouleurBoule


class Joueur:
    """
    Représente un joueur du jeu BounceBox.

    Attributs:
        nom (str): Nom du joueur
        couleur (CouleurBoule): Couleur du joueur (ROUGE ou BLEUE)
        score (int): Nombre de billes gagnées
        est_actif (bool): True si c'est le tour du joueur
        temps_limite_tour (float): Temps limite pour jouer un coup (en secondes)
    """

    def __init__(self, nom: str, couleur: CouleurBoule, temps_limite_tour=45.0):
        """
        Initialise un joueur.

        Args:
            nom (str): Nom du joueur
            couleur (CouleurBoule): Couleur du joueur (ROUGE ou BLEUE)
            temps_limite_tour (float): Temps limite pour jouer (par défaut 45 secondes)
        """
        if couleur not in [CouleurBoule.ROUGE, CouleurBoule.BLEUE]:
            raise ValueError("La couleur du joueur doit être ROUGE ou BLEUE")

        self.nom = nom
        self.couleur = couleur
        self.score = 0
        self.est_actif = False
        self.temps_limite_tour = temps_limite_tour
        self.temps_restant = temps_limite_tour

    def ajouter_point(self):
        """Ajoute un point au score du joueur."""
        self.score += 1

    def a_gagne(self, points_pour_gagner=5) -> bool:
        """
        Vérifie si le joueur a remporté la partie.

        Args:
            points_pour_gagner (int): Nombre de points pour gagner (par défaut 5)

        Returns:
            bool: True si le joueur a suffisamment de points
        """
        return self.score >= points_pour_gagner

    def reactiver_timer(self):
        """Réinitialise le timer du tour."""
        self.temps_restant = self.temps_limite_tour

    def diminuer_timer(self, dt):
        """
        Diminue le timer du tour.

        Args:
            dt (float): Intervalle de temps en secondes
        """
        self.temps_restant -= dt

    def le_temps_est_ecoule(self) -> bool:
        """
        Vérifie si le temps imparti pour le tour est écoulé.

        Returns:
            bool: True si le temps est écoulé
        """
        return self.temps_restant <= 0

    def obtenir_temps_restant(self) -> float:
        """
        Retourne le temps restant pour le tour (minimum 0).

        Returns:
            float: Temps restant en secondes
        """
        return max(0, self.temps_restant)

    def __repr__(self):
        """Représentation textuelle du joueur."""
        return f"Joueur({self.nom}, {self.couleur.value}, score={self.score})"

