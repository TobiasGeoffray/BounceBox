"""Classe principale orchestrant une partie de BounceBox (Version Fusionnée)."""

from enum import Enum
from typing import List, Tuple
from boule import Boule, Boule_blanche, Boule_de_couleur, CouleurBoule
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
                 points_pour_gagner=5, largeur_plateau=800, hauteur_plateau=600, avec_bot=False):
        """
        Initialise une partie.

        Args:
            nom_joueur1 (str): Nom du premier joueur (rouge)
            nom_joueur2 (str): Nom du second joueur (bleu)
            points_pour_gagner (int): Nombre de points pour gagner (par défaut 5)
            largeur_plateau (int): Largeur du plateau (par défaut 800)
            hauteur_plateau (int): Hauteur du plateau (par défaut 600)
            avec_bot (bool): True pour jouer contre un bot, False pour 2 joueurs (par défaut False)
        """
        self.plateau = Plateau(largeur_plateau, hauteur_plateau)
        self.joueur1 = Joueur(nom_joueur1, CouleurBoule.ROUGE)
        self.joueur2 = Joueur(nom_joueur2, CouleurBoule.BLEUE, est_bot=avec_bot)
        self.joueur_actif = self.joueur1  # Le rouge commence toujours
        self.etat = EtatPartie.DEBUT
        self.points_pour_gagner = points_pour_gagner
        self.boules_gagnees_ce_tour: List[Boule] = []
        self.collisions_ce_tour: List[Tuple[Boule, Boule]] = []
        self.avec_bot = avec_bot

        # compteur de suivi
        self.numero_tour = 1
        self.historique_tours = []
        self.temps_total_partie = 0.0

    def initialiser_boules(self):
        """Initialise les boules sur le plateau selon les règles du jeu (Modifications binôme)."""
        # Ajout de la boule blanche au centre
        boule_blanche = Boule_blanche(
            x=self.plateau.largeur / 2,
            y=self.plateau.hauteur / 2,
            rayon=10
        )
        self.plateau.ajouter_boule(boule_blanche)

        # Ajout de 9 boules grises
        for i in range(9):
            x = random.uniform(50, self.plateau.largeur - 50)
            y = random.uniform(50, self.plateau.hauteur - 50)
            boule_grise = Boule_de_couleur(x, y, CouleurBoule.GRISE, rayon=10)
            self.plateau.ajouter_boule(boule_grise)

        # Ajout de 2 boules bleues
        for i in range(2):
            x = random.uniform(50, self.plateau.largeur - 50)
            y = random.uniform(50, self.plateau.hauteur - 50)
            boule_bleue = Boule_de_couleur(x, y, CouleurBoule.BLEUE, rayon=10)
            self.plateau.ajouter_boule(boule_bleue)

    def lancer_boule_blanche(self, angle_degres: float, force: float):
        """
        Lance la boule blanche avec un angle et une force donnés.
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
                print(f"DEBUG: Tour fini, joueur actif est maintenant {self.joueur_actif.nom}")

    def passer_tour_timeout(self):
        """Le joueur passe son tour car le temps est écoulé."""
        if self.joueur_actif.le_temps_est_ecoule():
            self.finir_tour()

    def finir_tour(self):
        """Termine le tour actuel, enregistre ses statistiques et bascule au joueur suivant."""
        if self.etat == EtatPartie.ATTENTE or self.etat == EtatPartie.TOUR:

            # ⏱ Votre calcul du temps passé par le joueur pendant ce coup
            temps_joue = 0.0
            if hasattr(self.joueur_actif, 'temps_limite_tour') and hasattr(self.joueur_actif, 'temps_restant'):
                temps_joue = self.joueur_actif.temps_limite_tour - self.joueur_actif.temps_restant

            self.temps_total_partie += temps_joue

            #  Nombre de points gagnés pendant ce tour
            points_gagnes_ce_tour = len(self.boules_gagnees_ce_tour)

            # Structuration et enregistrement des données du tour actuel
            donnees_tour = {
                "tour": self.numero_tour,
                "joueur": self.joueur_actif.nom,
                "couleur": self.joueur_actif.couleur.value if hasattr(self.joueur_actif.couleur, 'value') else str(
                    self.joueur_actif.couleur),
                "temps_coup": round(temps_joue, 1),
                "points_gagnes": points_gagnes_ce_tour,
                "score_actuel_j1": self.joueur1.score,
                "score_actuel_j2": self.joueur2.score
            }
            self.historique_tours.append(donnees_tour)

            # Passage au numéro de tour suivant
            self.numero_tour += 1

            # Changer de joueur (Logique binôme)
            self.joueur_actif = self.joueur2 if self.joueur_actif == self.joueur1 else self.joueur1
            self.joueur_actif.reactiver_timer()
            self.tour_a_change = True
            self.etat = EtatPartie.TOUR
            self.boules_gagnees_ce_tour = []
            self.collisions_ce_tour = []
            self.changement_detecte = True

    def executer_coup_bot(self):
        """
        Exécute automatiquement le coup du bot si c'est son tour (Ajout binôme).
        Cette méthode doit être appelée à chaque frame quand c'est le tour du bot.
        """
        if self.etat != EtatPartie.TOUR or not self.joueur_actif.est_bot:
            return False

        # Le bot calcule son meilleur coup
        angle, force = self.joueur_actif.bot.calculer_meilleur_coup(self.plateau)

        # Lancer la boule blanche
        self.lancer_boule_blanche(angle, force)

        return True

    def demarrer_partie(self):
        """Démarre une nouvelle partie."""
        self.initialiser_boules()
        self.joueur1.reactiver_timer()
        self.joueur2.reactiver_timer()
        self.joueur_actif = self.joueur1
        self.etat = EtatPartie.TOUR

        # réinitialisation des compteurs pour la nouvelle partie
        self.numero_tour = 1
        self.historique_tours = []
        self.temps_total_partie = 0.0

    def obtenir_etat_partie(self) -> dict:
        """Retourne l'état complet de la partie pour affichage/debug."""
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

    def sauvegarder_statistiques(self):
        """
        Votre méthode de sauvegarde du résumé et du suivi complet dans un fichier CSV.
        """
        # SÉCURITÉ : Si aucun coup n'a été enregistré (fermeture immédiate), on évite un fichier vide
        if not hasattr(self, 'historique_tours') or not self.historique_tours:
            print("⚠️ Aucun coup n'a été enregistré dans cette session, écriture CSV annulée.")
            return

        import csv
        from datetime import datetime

        nom_fichier = "suivi_parties_bouncebox.csv"

        # Détermination du vainqueur
        if self.joueur1.a_gagne(self.points_pour_gagner):
            vainqueur = self.joueur1.nom
        elif self.joueur2.a_gagne(self.points_pour_gagner):
            vainqueur = self.joueur2.nom
        else:
            vainqueur = f"Interrompu (Score en cours: {self.joueur1.nom} {self.joueur1.score} - {self.joueur2.score} {self.joueur2.nom})"

        # Écriture dans le fichier CSV
        with open(nom_fichier, mode='a', newline='', encoding='utf-8') as fichier:
            writer = csv.writer(fichier, delimiter=';')

            writer.writerow([])
            writer.writerow(["=================================================="])
            writer.writerow([f"PARTIE DU {datetime.now().strftime('%d/%m/%Y à %H:%M')}"])
            writer.writerow(["=================================================="])

            # --- SECTION 1 : RÉSUMÉ GLOBAL ---
            writer.writerow(["--- RESUME DE LA PARTIE ---"])
            writer.writerow(["Joueur Rouge", self.joueur1.nom, "Score Final", self.joueur1.score])
            writer.writerow(["Joueur Bleu", self.joueur2.nom, "Score Final", self.joueur2.score])
            writer.writerow(["VAINQUEUR", vainqueur])
            writer.writerow(["TEMPS TOTAL (s)", round(self.temps_total_partie, 1)])
            writer.writerow([])

            # --- SECTION 2 : SUIVI TOUR PAR TOUR ---
            writer.writerow(["--- CHRONOLOGIE TOUR PAR TOUR ---"])
            writer.writerow([
                "Tour", "Joueur Actif", "Couleur", "Temps (s)",
                "Bille(s) Gagnée(s) ce tour", "Total Rouge", "Total Bleu"
            ])

            for t in self.historique_tours:
                writer.writerow([
                    f"Tour {t['tour']}",
                    t['joueur'],
                    t['couleur'],
                    t['temps_coup'],
                    t['points_gagnes'],
                    t['score_actuel_j1'],
                    t['score_actuel_j2']
                ])

        print(f"📊 Suivi détaillé exporté avec succès dans '{nom_fichier}'")

    def calculer_ligne_visee(self, angle_degres: float, force: float, rebonds_max=1) -> list:
        """
        Calcule de façon récursive la trajectoire prédictive de la boule blanche.
        BRIDÉE À 1 SEUL REBOND MAXIMUM.

        Retourne une liste de tuples (x, y) représentant les points de passage.
        """
        boule_blanche = self.plateau.obtenir_boule_blanche()
        if not boule_blanche:
            return []

        import math
        angle_radians = math.radians(angle_degres)

        # Calcul des vecteurs de vitesse initiaux virtuels
        vx = force * math.cos(angle_radians)
        vy = force * math.sin(angle_radians)

        # On initialise la liste avec la position de départ (la boule blanche)
        points_trajectoire = [(boule_blanche.x, boule_blanche.y)]

        return self._calculer_trajectoire_recursive(
            boule_blanche.x, boule_blanche.y,
            vx, vy,
            rebonds_max,  # Vaut 1 par défaut
            points_trajectoire
        )

    def _calculer_trajectoire_recursive(self, x, y, vx, vy, rebonds_restants, points) -> list:
        """
        Méthode privée récursive corrigée et blindée contre le crash 0xC0000409.
        S'arrête strictement dès que le quota de rebonds (ici 1) est atteint.
        """
        # SÉCURITÉ 1 : Arrêt immédiat si le quota de rebond est atteint
        if rebonds_restants <= 0:
            return points

        # SÉCURITÉ 2 : Si la vitesse est nulle ou quasi-nulle (inférieure à 0.1 pixel/s)
        # On stoppe tout pour éviter les divisions aberrantes par des nombres minuscules
        if abs(vx) < 0.1 and abs(vy) < 0.1:
            return points

        largeur = self.plateau.largeur
        hauteur = self.plateau.hauteur
        rayon = 10  # Rayon de la boule blanche

        t_mur = float('inf')
        mur_touche = None

        # --- CALCUL DU TEMPS AVANT L'IMPACT SUR LES MURS ---
        # On utilise un seuil de mouvement minimum (0.001) pour éviter les divisions par zéro
        if vx < -0.001:
            t = (rayon - x) / vx
            if t > 0.01 and t < t_mur: t_mur, mur_touche = t, 'vertical'
        elif vx > 0.001:
            t = (largeur - rayon - x) / vx
            if t > 0.01 and t < t_mur: t_mur, mur_touche = t, 'vertical'

        if vy < -0.001:
            t = (rayon - y) / vy
            if t > 0.01 and t < t_mur: t_mur, mur_touche = t, 'horizontal'
        elif vy > 0.001:
            t = (hauteur - rayon - y) / vy
            if t > 0.01 and t < t_mur: t_mur, mur_touche = t, 'horizontal'

        # SÉCURITÉ 3 : Si la trajectoire est parallèle à un mur ou ne rencontre rien rapidement
        if mur_touche is None or t_mur == float('inf') or t_mur > 2000:
            # On prolonge proprement la ligne droite sur une distance fixe de sécurité
            points.append((x + vx * 0.5, y + vy * 0.5))
            return points

        # --- ENREGISTREMENT DU POINT D'IMPACT ---
        nouvel_x = x + vx * t_mur
        nouvel_y = y + vy * t_mur
        points.append((nouvel_x, nouvel_y))

        # --- CALCUL DE LA VITESSE APRÈS LE REBOND ---
        if mur_touche == 'vertical':
            nouvelle_vx = -vx
            nouvelle_vy = vy
        else:
            nouvelle_vx = vx
            nouvelle_vy = -vy

        # Amortissement de la bande (90% de l'énergie conservée)
        nouvelle_vx *= 0.9
        nouvelle_vy *= 0.9

        # SÉCURITÉ 4 : On décale numériquement la bille du mur pour le cycle suivant
        sec_x = nouvel_x + (nouvelle_vx * 0.02)
        sec_y = nouvel_y + (nouvelle_vy * 0.02)

        # Appel récursif (rebonds_restants passe à 0, assurant l'arrêt au début du prochain appel)
        return self._calculer_trajectoire_recursive(
            sec_x, sec_y,
            nouvelle_vx, nouvelle_vy,
            rebonds_restants - 1,
            points
        )