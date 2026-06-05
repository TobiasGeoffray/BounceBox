"""Classe Bot pour jouer automatiquement contre le joueur humain."""

import math
import copy
from typing import Tuple, List
from boule import Boule, Boule_blanche, Boule_de_couleur, CouleurBoule
from plateau import Plateau
from impact import Impact


class Bot:
    """
    Bot joueur capable de jouer au BounceBox en utilisant l'algorithme min-max.

    Le bot teste différents angles (pas de 5°) et puissances (pas de 10%)
    pour trouver le meilleur coup selon le scoring:
    - 0 points: aucune boule touchée
    - 1 point par boule grise touchée
    - 2 points: boule adverse touchée
    - 3 points: boule de la couleur du joueur touchée
    """

    def __init__(self, couleur_joueur: CouleurBoule):
        """
        Initialise le bot.

        Args:
            couleur_joueur (CouleurBoule): Couleur du joueur bot (ROUGE ou BLEUE)
        """
        self.couleur_joueur = couleur_joueur
        self.pas_angle = 5  # 5 degrés
        self.pas_puissance = 10  # 10% de puissance

    def _construire_angles_valides(self, plateau: Plateau) -> List[int]:
        """
        Construit la liste des angles (degrés) qui peuvent atteindre au moins
        une boule directement ou après un unique rebond (1 rebond autorisé)

        Utilise la méthode des intervalles angulaires pour chaque boule et
        ajoute aussi les intervalles des images réfléchies par rapport aux
        quatre bordures (méthode image) afin de prendre en compte 1 rebond.
        """
        boule_blanche = plateau.obtenir_boule_blanche()
        if not boule_blanche:
            return []

        A = int(360 // self.pas_angle)
        marks = [0] * (A + 1)  # arbre de différence pour marquer intervalles
        eps = 1e-9
        two_pi = 2.0 * math.pi

        def ang_to_index(angle_rad: float) -> int:
            # normaliser en [0, 2pi)
            a = angle_rad % two_pi
            return int(math.floor((a * A) / two_pi))

        def ajouter_intervalle(centre_rad: float, ouverture_rad: float):
            start = ang_to_index(centre_rad - ouverture_rad)
            end = ang_to_index(centre_rad + ouverture_rad)
            if start <= end:
                marks[start] += 1
                marks[end + 1] -= 1
            else:
                # wrap-around
                marks[start] += 1
                marks[A] -= 1
                marks[0] += 1
                marks[end + 1] -= 1

        # paramètres des bordures (pour images)
        left_x = plateau.limite_gauche
        right_x = plateau.limite_droite
        top_y = plateau.limite_haut
        bottom_y = plateau.limite_bas

        px, py = boule_blanche.x, boule_blanche.y

        for boule in plateau.boules:
            if boule is None:
                continue
            if boule.couleur == CouleurBoule.BLANCHE:
                continue

            # Direct
            vx = boule.x - px
            vy = boule.y - py
            d = math.hypot(vx, vy)
            if d <= boule.rayon + eps:
                # tout angle possible
                marks[0] += 1
                marks[A] -= 1
            else:
                ouverture = math.asin(min(1.0, boule.rayon / d))
                centre = math.atan2(vy, vx)
                ajouter_intervalle(centre, ouverture)

            # Images pour 1 rebond: réfléchir la position de la boule par rapport
            # à chaque bordure et ajouter son intervalle.
            # Mur gauche
            img_x = 2 * left_x - boule.x
            img_y = boule.y
            vx_img = img_x - px
            vy_img = img_y - py
            d_img = math.hypot(vx_img, vy_img)
            if d_img > eps:
                ouverture_img = math.asin(min(1.0, boule.rayon / d_img))
                centre_img = math.atan2(vy_img, vx_img)
                ajouter_intervalle(centre_img, ouverture_img)

            # Mur droit
            img_x = 2 * right_x - boule.x
            img_y = boule.y
            vx_img = img_x - px
            vy_img = img_y - py
            d_img = math.hypot(vx_img, vy_img)
            if d_img > eps:
                ouverture_img = math.asin(min(1.0, boule.rayon / d_img))
                centre_img = math.atan2(vy_img, vx_img)
                ajouter_intervalle(centre_img, ouverture_img)

            # Mur haut
            img_x = boule.x
            img_y = 2 * top_y - boule.y
            vx_img = img_x - px
            vy_img = img_y - py
            d_img = math.hypot(vx_img, vy_img)
            if d_img > eps:
                ouverture_img = math.asin(min(1.0, boule.rayon / d_img))
                centre_img = math.atan2(vy_img, vx_img)
                ajouter_intervalle(centre_img, ouverture_img)

            # Mur bas
            img_x = boule.x
            img_y = 2 * bottom_y - boule.y
            vx_img = img_x - px
            vy_img = img_y - py
            d_img = math.hypot(vx_img, vy_img)
            if d_img > eps:
                ouverture_img = math.asin(min(1.0, boule.rayon / d_img))
                centre_img = math.atan2(vy_img, vx_img)
                ajouter_intervalle(centre_img, ouverture_img)

        # Construire la liste d'angles valides à partir des marks (préfix sum)
        valid_angles: List[int] = []
        s = 0
        for i in range(A):
            s += marks[i]
            if s > 0:
                angle_deg = int(i * self.pas_angle)
                if angle_deg > 180 :
                    angle_deg = angle_deg - 360
                valid_angles.append(angle_deg)

        return valid_angles

    def calculer_meilleur_coup(self, plateau: Plateau) -> Tuple[float, float]:
        """
        Calcule le meilleur coup à jouer selon l'algorithme min-max.

        Args:
            plateau (Plateau): Le plateau de jeu actuel

        Returns:
            Tuple[float, float]: (angle_degres, force) du meilleur coup
        """
        meilleur_angle = 0
        meilleur_force = 10
        meilleur_score = -float('inf')

        # Pré-filtrer les angles : ne garder que ceux qui peuvent atteindre
        # une boule directement ou après un rebond (1 rebond autorisé)
        angles_valides = self._construire_angles_valides(plateau)
        print(angles_valides)
        # Si le pré-filtre retire tout (cas rare), retomber sur tous les angles
        if not angles_valides:
            angles_iterable = range(0, 360, self.pas_angle)
        else:
            angles_iterable = angles_valides

        # Tester tous les angles filtrés
        for angle in angles_iterable:
            # Tester toutes les puissances
            for puissance_pct in range(self.pas_puissance, 301, self.pas_puissance):
                force = puissance_pct  # Convertir en force (1.0 * puissance_pct / 100 * 10)

                # Évaluer ce coup
                score = self._evaluer_coup(plateau, angle, force)

                # Garder le meilleur score
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_angle = angle
                    meilleur_force = force
                if score >= 6 :
                    print('🎳 Très bon coup trouvé!! Pas besoin de chercher plus!')
                    return meilleur_angle, meilleur_force

        return meilleur_angle, meilleur_force

    def _evaluer_coup(self, plateau: Plateau, angle_degres: float, force: float) -> int:
        """
        Évalue un coup en simulant son résultat.

        Args:
            plateau (Plateau): Le plateau de jeu
            angle_degres (float): Angle du coup en degrés
            force (float): Force du coup

        Returns:
            int: Score du coup
        """
        # Créer une copie du plateau pour la simulation
        plateau_copie = self._copier_plateau(plateau)

        # Appliquer le coup
        boule_blanche = plateau_copie.obtenir_boule_blanche()
        if not boule_blanche:
            return 0

        # Convertir l'angle en radians et appliquer la force
        angle_radians = math.radians(angle_degres)
        boule_blanche.vx = force * math.cos(angle_radians)
        boule_blanche.vy = force * math.sin(angle_radians)

        # Simuler jusqu'à ce que toutes les boules s'arrêtent
        score = self._simuler_et_scorer(plateau_copie)

        return score

    def _simuler_et_scorer(self, plateau: Plateau, max_iterations=5000) -> int:
        """
        Simule le coup et retourne le score obtenu.

        Args:
            plateau (Plateau): Plateau à simuler
            max_iterations (int): Nombre max d'itérations de simulation

        Returns:
            int: Score total du coup
        """
        score = 0
        boule_blanche = plateau.obtenir_boule_blanche()
        boules_frappees = set()

        for _ in range(max_iterations):
            # Mettre à jour le plateau
            plateau.mettre_a_jour(0.016)  # ~60 FPS

            # Détecter les collisions avec la boule blanche
            collisions = Impact.detecter_et_resoudre_collisions_boules(plateau.boules)

            # Traiter les collisions pour le scoring
            for boule_b, boule_touchee in collisions:
                if boule_b == boule_blanche and boule_touchee not in boules_frappees:
                    boules_frappees.add(boule_touchee)
                    score += self._scorer_collision(boule_touchee)

            # Arrêter si toutes les boules sont immobiles
            if all(boule.est_arrêtee() for boule in plateau.boules):
                break

        return score

    def _scorer_collision(self, boule_touchee: Boule) -> int:
        """
        Retourne le score pour une collision avec une boule.

        Scoring:
        - 1 point par boule grise touchée
        - 2 points: boule adverse touchée
        - 3 points: boule de la couleur du joueur touchée

        Args:
            boule_touchee (Boule): La boule touchée

        Returns:
            int: Score de la collision
        """
        if boule_touchee.couleur == CouleurBoule.GRISE:
            return 1
        elif boule_touchee.couleur == self.couleur_joueur:
            return 4
        elif boule_touchee.couleur in [CouleurBoule.ROUGE, CouleurBoule.BLEUE]:
            # Boule adverse
            return 2
        else:
            return 0

    def _copier_plateau(self, plateau: Plateau) -> Plateau:
        """
        Crée une copie profonde du plateau pour la simulation.

        Args:
            plateau (Plateau): Plateau à copier

        Returns:
            Plateau: Nouveau plateau avec copies de tous les éléments
        """
        nouveau_plateau = Plateau(
            plateau.largeur,
            plateau.hauteur,
            plateau.coefficient_resistance,
            plateau.coefficient_bounce
        )

        # Copier les boules
        for boule in plateau.boules:
            boule_copie = copy.copy(boule)
            nouveau_plateau.ajouter_boule(boule_copie)

        return nouveau_plateau

    def __repr__(self):
        """Représentation textuelle du bot."""
        return f"Bot({self.couleur_joueur.value}, pas_angle={self.pas_angle}°, pas_puissance={self.pas_puissance}%)"

