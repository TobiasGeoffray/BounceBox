"""GameWidget : Affichage et interaction avec le plateau de jeu."""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
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
        self.game_thread.board_update.connect(self.update)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        plateau = self.game_thread.get_plateau()

        # Plateau
        painter.fillRect(0, 0, 800, 600, QColor(30, 120, 50))
        painter.setPen(QPen(QColor(100, 60, 20), 15))
        painter.drawRect(7, 7, 786, 586)

        # Boules
        for b in plateau.boules:
            x = int(b.x - b.rayon)
            y = int(b.y - b.rayon)
            diam = b.rayon * 2

            # Remplissage
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.COLORS.get(b.couleur, QColor(200,200,200))))
            painter.drawEllipse(x, y, diam, diam)

            # Bordure
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(x, y, diam, diam)

        # Guide de visée
        if self.is_aiming and self.aim_current:
            painter.setPen(QPen(QColor(255, 255, 0), 2, Qt.DashLine))
            painter.drawLine(self.aim_start, self.aim_current)

            dist = math.sqrt((self.aim_current.x()-self.aim_start.x())**2 +
                            (self.aim_current.y()-self.aim_start.y())**2)
            angle = math.degrees(math.atan2(self.aim_current.y()-self.aim_start.y(),
                                           self.aim_current.x()-self.aim_start.x()))
            force = min(300, dist/150*300)

            painter.setFont(QFont('Arial', 10))
            painter.setPen(QPen(QColor(255, 255, 0)))
            painter.drawText(10, 30, f"Angle: {angle:.0f}° | Force: {force:.0f}%")
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            plateau = self.game_thread.get_plateau()
            wb = plateau.obtenir_boule_blanche()
            if wb and math.sqrt((event.x()-wb.x)**2 + (event.y()-wb.y)**2) < 50:
                self.is_aiming = True
                self.aim_start = event.pos()
                self.aim_current = event.pos()
    def mouseMoveEvent(self, event):
        if self.is_aiming:
            self.aim_current = event.pos()
            self.update()
    def mouseReleaseEvent(self, event):
        if self.is_aiming and event.button() == Qt.LeftButton:
            self.is_aiming = False
            dist = math.sqrt((self.aim_current.x()-self.aim_start.x())**2 +
                            (self.aim_current.y()-self.aim_start.y())**2)
            angle = math.degrees(math.atan2(self.aim_current.y()-self.aim_start.y(),
                                           self.aim_current.x()-self.aim_start.x()))
            # Augmenter la force maximale pour que les boules aillent plus loin
            force = min(300, dist/150*300)  # Augmenté de 100 à 300
            if force > 5:
                self.ball_launch_requested.emit(angle, force)
