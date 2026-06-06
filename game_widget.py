"""
GameWidget : Interface graphique de la table de billard.
Version avec Force augmentée et Prédiction de multi-rebonds (2 rebonds).
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
import math
from boule import CouleurBoule

class GameWidget(QWidget):
    ball_launch_requested = pyqtSignal(float, float)

    def __init__(self, game_thread):
        super().__init__()
        self.game_thread = game_thread
        self.setMinimumSize(800, 600)

        self.COLORS = {
            CouleurBoule.BLANCHE: QColor(255, 255, 255),
            CouleurBoule.GRISE: QColor(150, 150, 150),
            CouleurBoule.ROUGE: QColor(220, 50, 50),
            CouleurBoule.BLEUE: QColor(50, 100, 220),
        }

        self.is_aiming = False
        self.aim_start = None
        self.aim_current = None

        self.angle_actuel = 0.0
        self.force_actuelle = 0.0

        self.game_thread.board_update.connect(self.update)

    def simuler_un_rebond_graphique(self, start_x, start_y, angle_degres, liste_boules, boule_blanche, nb_rebonds=2) -> list:
        """
        Calcule la trajectoire prédictive de la bille blanche sur plusieurs rebonds consécutifs
        en se basant sur les formules physiques de la classe Impact.
        """
        points = [(start_x, start_y)]

        angle_rad = math.radians(angle_degres)
        vx = math.cos(angle_rad)
        vy = math.sin(angle_rad)

        if abs(vx) < 0.001 and abs(vy) < 0.001:
            return points

        limite_gauche = 15 + 10
        limite_droite = 800 - 15 - 10
        limite_haute = 15 + 10
        limite_basse = 600 - 15 - 10

        current_x = start_x
        current_y = start_y

        # Boucle pour calculer le nombre d'impacts successifs
        for _ in range(nb_rebonds):
            t_min = float('inf')
            type_impact = None
            boule_touchee = None

            # 1. RECHERCHE D'IMPACT SUR LES MURS
            if vx > 0:
                t = (limite_droite - current_x) / vx
                if 0 < t < t_min: t_min, type_impact = t, 'V'
            elif vx < 0:
                t = (limite_gauche - current_x) / vx
                if 0 < t < t_min: t_min, type_impact = t, 'V'

            if vy > 0:
                t = (limite_basse - current_y) / vy
                if 0 < t < t_min: t_min, type_impact = t, 'H'
            elif vy < 0:
                t = (limite_haute - current_y) / vy
                if 0 < t < t_min: t_min, type_impact = t, 'H'

            # 2. RECHERCHE D'IMPACT SUR LES AUTRES BOULES
            rayon_collision = boule_blanche.rayon * 2

            for b in liste_boules:
                if b == boule_blanche:
                    continue

                # Distance depuis la position de départ du segment en cours
                dx = current_x - b.x
                dy = current_y - b.y

                coef_b = 2 * (dx * vx + dy * vy)
                coef_c = (dx ** 2 + dy ** 2) - (rayon_collision ** 2)

                discriminant = (coef_b ** 2) - (4 * coef_c)

                if discriminant >= 0:
                    t1 = (-coef_b - math.sqrt(discriminant)) / 2
                    # Le point d'impact doit être devant nous (> 0.1 pour éviter de ré-impacter la même bille)
                    if 0.1 < t1 < t_min:
                        t_min = t1
                        type_impact = 'B'
                        boule_touchee = b

            # Si aucun obstacle n'est sur la trajectoire, on projette loin et on arrête
            if type_impact is None or t_min == float('inf'):
                points.append((current_x + vx * 300, current_y + vy * 300))
                break

            # Calcul du point d'impact trouvé lors de cette étape
            impact_x = current_x + vx * t_min
            impact_y = current_y + vy * t_min
            points.append((impact_x, impact_y))

            # 3. RÉSOLUTION DE LA NOUVELLE DIRECTION POUR LE PROCHAIN REBOND
            if type_impact == 'V':
                vx, vy = -vx, vy
            elif type_impact == 'H':
                vx, vy = vx, -vy
            elif type_impact == 'B' and boule_touchee:
                dx_choc = boule_touchee.x - impact_x
                dy_choc = boule_touchee.y - impact_y
                distance_choc = math.sqrt(dx_choc ** 2 + dy_choc ** 2)

                if distance_choc > 0:
                    nx = dx_choc / distance_choc
                    ny = dy_choc / distance_choc

                    dvx = -vx
                    dvy = -vy
                    dvn = dvx * nx + dvy * ny

                    if dvn < 0:
                        impulsion = -dvn / (boule_blanche.masse + boule_touchee.masse)
                        vx = vx - (impulsion * boule_blanche.masse * nx)
                        vy = vy - (impulsion * boule_blanche.masse * ny)

            # Pour l'itération suivante, le départ devient le point d'impact actuel
            current_x = impact_x
            current_y = impact_y

        # Si le dernier segment calculé n'a pas touché d'obstacle final, on ajoute une petite ligne de fin
        if len(points) == nb_rebonds + 1:
            points.append((current_x + vx * 150, current_y + vy * 150))

        return points

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        try:
            plateau = self.game_thread.get_plateau()
            partie = self.game_thread.get_partie()
        except AttributeError:
            return

        if not plateau or not partie:
            return

        # Rendu tapis
        painter.fillRect(0, 0, 800, 600, QColor(30, 120, 50))
        painter.setPen(QPen(QColor(100, 60, 20), 15))
        painter.drawRect(7, 7, 786, 586)

        # Recherche de la blanche
        boule_blanche_obj = None
        for b in plateau.boules:
            if b.couleur == CouleurBoule.BLANCHE:
                boule_blanche_obj = b
                break

        # Dessin des boules
        for b in plateau.boules:
            x = int(b.x - b.rayon)
            y = int(b.y - b.rayon)
            diam = b.rayon * 2
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.COLORS.get(b.couleur, QColor(200, 200, 200))))
            painter.drawEllipse(x, y, diam, diam)
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(x, y, diam, diam)

        # Affichage visée
        if partie.joueur_actif.est_bot:
            painter.setFont(QFont('Arial', 14, QFont.Bold))
            painter.setPen(QPen(QColor(255, 200, 0)))
            painter.drawText(10, 50, f"🤖 {partie.joueur_actif.nom} réfléchit...")
        else:
            if self.is_aiming and self.aim_current and self.aim_start and boule_blanche_obj:
                painter.setPen(QPen(QColor(255, 255, 0), 1, Qt.DashLine))
                painter.drawLine(self.aim_start, self.aim_current)

                painter.setFont(QFont('Arial', 10))
                painter.setPen(QPen(QColor(255, 255, 0)))
                painter.drawText(10, 30, f"Angle: {self.angle_actuel:.0f}° | Force: {self.force_actuelle:.0f}%")

                if self.force_actuelle > 5:
                    # Simulation demandant l'analyse de 2 rebonds successifs
                    trajectoire = self.simuler_un_rebond_graphique(
                        boule_blanche_obj.x, boule_blanche_obj.y, self.angle_actuel, plateau.boules, boule_blanche_obj, nb_rebonds=2
                    )

                    # Dessin dynamique de tous les segments calculés
                    if isinstance(trajectoire, list) and len(trajectoire) >= 2:
                        for i in range(len(trajectoire) - 1):
                            p_start = trajectoire[i]
                            p_end = trajectoire[i+1]

                            # Le premier segment est en ligne continue, les suivants en pointillés
                            if i == 0:
                                painter.setPen(QPen(QColor(255, 255, 255, 200), 2, Qt.SolidLine))
                            else:
                                painter.setPen(QPen(QColor(255, 255, 255, 160), 2, Qt.DashLine))

                            painter.drawLine(int(p_start[0]), int(p_start[1]), int(p_end[0]), int(p_end[1]))

                            # Dessiner un point d'impact rouge à chaque intersection (sauf le dernier point d'arrêt)
                            if i < len(trajectoire) - 2:
                                painter.setPen(Qt.NoPen)
                                painter.setBrush(QBrush(QColor(230, 50, 50, 255)))
                                painter.drawEllipse(int(p_end[0]) - 4, int(p_end[1]) - 4, 8, 8)

    def mousePressEvent(self, event):
        if self.game_thread.get_partie().joueur_actif.est_bot:
            return
        if event.button() == Qt.LeftButton:
            plateau = self.game_thread.get_plateau()
            wb = plateau.obtenir_boule_blanche()
            if wb and math.sqrt((event.x() - wb.x) ** 2 + (event.y() - wb.y) ** 2) < 50:
                self.is_aiming = True
                self.aim_start = event.pos()
                self.aim_current = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_aiming:
            self.aim_current = event.pos()
            dist = math.sqrt((self.aim_current.x() - self.aim_start.x()) ** 2 +
                             (self.aim_current.y() - self.aim_start.y()) ** 2)
            self.angle_actuel = math.degrees(math.atan2(self.aim_start.y() - self.aim_current.y(),
                                                        self.aim_start.x() - self.aim_current.x()))

            # Limite augmentée à 400 pour des coups plus puissants
            self.force_actuelle = min(500, (dist / 200) * 500)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_aiming and event.button() == Qt.LeftButton:
            self.is_aiming = False
            if self.force_actuelle > 5:
                self.ball_launch_requested.emit(self.angle_actuel, self.force_actuelle)
            self.update()