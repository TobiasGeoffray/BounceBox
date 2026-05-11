"""Classe principale orchestrant une partie de BounceBox."""

from enum import Enum
from typing import List, Tuple
from boule import Boule, CouleurBoule
from plateau import Plateau
from joueur import Joueur
from impact import Impact
import random


class EtatPartie(Enum):
    """Énumération des états possibles d'une partie."""
    DEBUT = "debut"
    TOUR = "tour"
    ATTENTE = "attente"
    FIN = "fin"


class Partie:
    """
    Orchestre une partie complète de BounceBox.

    Attributs:
        plateau (Plateau): Le plateau de jeu
        joueur1 (Joueur): Joueur 1 (toujours rouge)
        joueur2 (Joueur): Joueur 2 (toujours bleu)
        joueur_actif (Joueur): Joueur dont c'est le tour
        etat (EtatPartie): État actuel de la partie
        points_pour_gagner (int): Nombre de points pour remporter la partie
    """

    def __init__(self, nom_joueur1="Joueur 1", nom_joueur2="Joueur 2",
                 points_pour_gagner=5, largeur_plateau=800, hauteur_plateau=600):
        """
        Initialise une partie.

        Args:
            nom_joueur1 (str): Nom du premier joueur (rouge)
            nom_joueur2 (str): Nom du second joueur (bleu)
            points_pour_gagner (int): Nombre de points pour gagner (par défaut 5)
            largeur_plateau (int): Largeur du plateau (par défaut 800)
            hauteur_plateau (int): Hauteur du plateau (par défaut 600)
        """
        self.plateau = Plateau(largeur_plateau, hauteur_plateau)
        self.joueur1 = Joueur(nom_joueur1, CouleurBoule.ROUGE)
        self.joueur2 = Joueur(nom_joueur2, CouleurBoule.BLEUE)
        self.joueur_actif = self.joueur1  # Le rouge commence toujours
        self.etat = EtatPartie.DEBUT
        self.points_pour_gagner = points_pour_gagner
        self.boules_gagnees_ce_tour: List[Boule] = []
        self.collisions_ce_tour: List[Tuple[Boule, Boule]] = []

    def initialiser_boules(self):
        """Initialise les boules sur le plateau selon les règles du jeu."""
        # Ajout de la boule blanche au centre
        boule_blanche = Boule(
            x=self.plateau.largeur / 2,
            y=self.plateau.hauteur / 2,
            couleur=CouleurBoule.BLANCHE,
            rayon=10
        )
        self.plateau.ajouter_boule(boule_blanche)

        # Ajout de 9 boules grises
        for i in range(9):
            x = random.uniform(50, self.plateau.largeur - 50)
            y = random.uniform(50, self.plateau.hauteur - 50)
            boule_grise = Boule(x, y, CouleurBoule.GRISE, rayon=10)
            self.plateau.ajouter_boule(boule_grise)

        # Ajout de 2 boules bleues
        for i in range(2):
            x = random.uniform(50, self.plateau.largeur - 50)
            y = random.uniform(50, self.plateau.hauteur - 50)
            boule_bleue = Boule(x, y, CouleurBoule.BLEUE, rayon=10)
            self.plateau.ajouter_boule(boule_bleue)

    def lancer_boule_blanche(self, angle_degres: float, force: float):
        """
        Lance la boule blanche avec un angle et une force donnés.

        Args:
            angle_degres (float): Angle de lancement en degrés (0 = droite, 90 = haut)
            force (float): Force du lancement (détermine la vitesse initiale)
        """
        if self.etat != EtatPartie.TOUR:
            raise RuntimeError("Impossible de lancer : ce n'est pas le moment")

        boule_blanche = self.plateau.obtenir_boule_blanche()
        if not boule_blanche:
            raise RuntimeError("Boule blanche non trouvée")

        # Conversion angle en radians
        import math
        angle_radians = math.radians(angle_degres)

        # Application de la force
        vitesse = force
        boule_blanche.vx = vitesse * math.cos(angle_radians)
        boule_blanche.vy = vitesse * math.sin(angle_radians)

        self.etat = EtatPartie.ATTENTE
        self.boules_gagnees_ce_tour = []
        self.collisions_ce_tour = []

    def mettre_a_jour_simulation(self, dt=0.016):
        """
        Met à jour la simulation du jeu (déplacement, collisions, etc.).

        Args:
            dt (float): Intervalle de temps (par défaut ~60 FPS)
        """
        if self.etat == EtatPartie.ATTENTE:
            # Mettre à jour le plateau (déplacement, rebonds, résistance)
            self.plateau.mettre_a_jour(dt)

            # Détecter et résoudre les collisions
            collisions = Impact.detecter_et_resoudre_collisions_boules(self.plateau.boules)
            self.collisions_ce_tour.extend(collisions)

            # Traiter les règles de couleur pour chaque collision avec la boule blanche
            boule_blanche = self.plateau.obtenir_boule_blanche()
            for boule_b, boule_touchee in collisions:
                if boule_b == boule_blanche:
                    resultat = Impact.appliquer_regle_couleur(
                        boule_blanche, boule_touchee, self.joueur_actif.couleur
                    )

                    if resultat == "gagne":
                        self.joueur_actif.ajouter_point()
                        self.plateau.retirer_boule(boule_touchee)
                        self.boules_gagnees_ce_tour.append(boule_touchee)

            # Vérifier si la partie est terminée
            if self.joueur_actif.a_gagne(self.points_pour_gagner):
                self.etat = EtatPartie.FIN
            # Vérifier si toutes les boules sont arrêtées
            elif all(boule.est_arrêtee() for boule in self.plateau.boules):
                self.finir_tour()

    def passer_tour_timeout(self):
        """Le joueur passe son tour car le temps est écoulé."""
        if self.joueur_actif.le_temps_est_ecoule():
            self.finir_tour()

    def finir_tour(self):
        """Termine le tour actuel et bascule au joueur suivant."""
        if self.etat == EtatPartie.ATTENTE or self.etat == EtatPartie.TOUR:
            # Changer de joueur
            self.joueur_actif = self.joueur2 if self.joueur_actif == self.joueur1 else self.joueur1
            self.joueur_actif.reactiver_timer()
            self.etat = EtatPartie.TOUR
            self.boules_gagnees_ce_tour = []
            self.collisions_ce_tour = []

    def demarrer_partie(self):
        """Démarre une nouvelle partie."""
        self.initialiser_boules()
        self.joueur1.reactiver_timer()
        self.joueur2.reactiver_timer()
        self.joueur_actif = self.joueur1
        self.etat = EtatPartie.TOUR

    def obtenir_etat_partie(self) -> dict:
        """
        Retourne l'état complet de la partie pour affichage/debug.

        Returns:
            dict: Dictionnaire contenant l'état de la partie
        """
        return {
            "etat": self.etat.value,
            "joueur_actif": self.joueur_actif.nom,
            "score_j1": self.joueur1.score,
            "score_j2": self.joueur2.score,
            "nombre_boules": len(self.plateau.boules),
        }

    def __repr__(self):
        """Représentation textuelle de la partie."""
        return f"Partie({self.joueur1.nom} vs {self.joueur2.nom}, score {self.joueur1.score}-{self.joueur2.score})"

