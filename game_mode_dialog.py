"""GameModeDialog : Dialogue de sélection du mode de jeu."""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QSpinBox, QGroupBox, QRadioButton,
                             QButtonGroup, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


class GameModeDialog(QDialog):
    """
    Dialogue permettant à l'utilisateur de choisir:
    - Mode de jeu (contre bot ou 2 joueurs humains)
    - Noms des joueurs
    - Points pour gagner
    """

    # Signal qui retourne les paramètres de la partie
    game_started = pyqtSignal(dict)

    def __init__(self, parent=None):
        """
        Initialise le dialogue.

        Args:
            parent: Fenêtre parente
        """
        super().__init__(parent)
        self.setWindowTitle("BounceBox - Sélection du Mode de Jeu")
        self.setGeometry(100, 100, 600, 500)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout()

        # Titre
        title = QLabel("BounceBox - Mode de Jeu")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Sélection du mode
        mode_group = QGroupBox("Mode de Jeu")
        mode_layout = QVBoxLayout()

        self.mode_buttons = QButtonGroup()

        self.radio_2players = QRadioButton("2 Joueurs Humains")
        self.radio_bot = QRadioButton("Jouer contre le Bot IA")

        self.mode_buttons.addButton(self.radio_2players, 0)
        self.mode_buttons.addButton(self.radio_bot, 1)

        self.radio_2players.setChecked(True)

        # Connecter les changements
        self.radio_2players.toggled.connect(self.on_mode_changed)
        self.radio_bot.toggled.connect(self.on_mode_changed)

        mode_layout.addWidget(self.radio_2players)
        mode_layout.addWidget(self.radio_bot)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Section des joueurs
        players_group = QGroupBox("Noms des Joueurs")
        players_layout = QVBoxLayout()

        # Joueur 1
        player1_layout = QHBoxLayout()
        player1_label = QLabel("Joueur 1 (ROUGE):")
        player1_label.setMinimumWidth(150)
        self.player1_input = QLineEdit("Joueur 1")
        player1_layout.addWidget(player1_label)
        player1_layout.addWidget(self.player1_input)
        players_layout.addLayout(player1_layout)

        # Joueur 2
        player2_layout = QHBoxLayout()
        self.player2_label = QLabel("Joueur 2 (BLEU):")
        self.player2_label.setMinimumWidth(150)
        self.player2_input = QLineEdit("Joueur 2")
        player2_layout.addWidget(self.player2_label)
        player2_layout.addWidget(self.player2_input)
        players_layout.addLayout(player2_layout)

        players_group.setLayout(players_layout)
        layout.addWidget(players_group)

        # Points pour gagner
        points_layout = QHBoxLayout()
        points_label = QLabel("Points pour Gagner:")
        points_label.setMinimumWidth(150)
        self.points_spinbox = QSpinBox()
        self.points_spinbox.setMinimum(1)
        self.points_spinbox.setMaximum(20)
        self.points_spinbox.setValue(5)
        points_layout.addWidget(points_label)
        points_layout.addWidget(self.points_spinbox)
        points_layout.addStretch()
        layout.addLayout(points_layout)

        # Boutons de contrôle
        button_layout = QHBoxLayout()

        btn_start = QPushButton("Démarrer la Partie")
        btn_start.setMinimumHeight(40)
        btn_start_font = QFont()
        btn_start_font.setPointSize(12)
        btn_start_font.setBold(True)
        btn_start.setFont(btn_start_font)
        btn_start.clicked.connect(self.start_game)

        btn_cancel = QPushButton("Annuler")
        btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(btn_start)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_mode_changed(self):
        """Appelé quand le mode de jeu change."""
        if self.radio_bot.isChecked():
            self.player2_label.setText("Bot IA (BLEU):")
            self.player2_input.setText("Bot IA")
            self.player2_input.setEnabled(False)
        else:
            self.player2_label.setText("Joueur 2 (BLEU):")
            self.player2_input.setText("Joueur 2")
            self.player2_input.setEnabled(True)

    def start_game(self):
        """Démarre la partie avec les paramètres sélectionnés."""
        player1_name = self.player1_input.text().strip()
        player2_name = self.player2_input.text().strip()
        points = self.points_spinbox.value()
        is_bot = self.radio_bot.isChecked()

        # Validations
        if not player1_name:
            QMessageBox.warning(self, "Erreur", "Le nom du joueur 1 ne peut pas être vide!")
            return

        if not player2_name:
            QMessageBox.warning(self, "Erreur", "Le nom du joueur 2 ne peut pas être vide!")
            return

        # Émettre le signal avec les paramètres
        self.game_started.emit({
            'player1_name': player1_name,
            'player2_name': player2_name,
            'points_to_win': points,
            'with_bot': is_bot
        })

        self.accept()


class SettingsDialog(QDialog):
    """
    Dialogue de configuration avancée du bot.
    Permet de régler la difficulté du bot.
    """

    settings_confirmed = pyqtSignal(dict)

    def __init__(self, parent=None):
        """Initialise le dialogue de paramètres."""
        super().__init__(parent)
        self.setWindowTitle("Paramètres du Bot")
        self.setGeometry(100, 100, 400, 250)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout()

        # Titre
        title = QLabel("Paramètres du Bot IA")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Pas d'angle
        angle_layout = QHBoxLayout()
        angle_label = QLabel("Précision des angles (degrés):")
        angle_label.setMinimumWidth(200)
        self.angle_spinbox = QSpinBox()
        self.angle_spinbox.setMinimum(1)
        self.angle_spinbox.setMaximum(45)
        self.angle_spinbox.setValue(5)
        self.angle_spinbox.setSuffix("°")
        angle_layout.addWidget(angle_label)
        angle_layout.addWidget(self.angle_spinbox)
        angle_layout.addStretch()
        layout.addLayout(angle_layout)

        # Pas de puissance
        power_layout = QHBoxLayout()
        power_label = QLabel("Précision de la puissance (%):")
        power_label.setMinimumWidth(200)
        self.power_spinbox = QSpinBox()
        self.power_spinbox.setMinimum(1)
        self.power_spinbox.setMaximum(50)
        self.power_spinbox.setValue(10)
        self.power_spinbox.setSuffix("%")
        power_layout.addWidget(power_label)
        power_layout.addWidget(self.power_spinbox)
        power_layout.addStretch()
        layout.addLayout(power_layout)

        # Info
        info_label = QLabel("Plus petit = plus fort mais plus lent")
        info_font = QFont()
        info_font.setItalic(True)
        info_font.setPointSize(9)
        info_label.setFont(info_font)
        layout.addWidget(info_label)

        layout.addStretch()

        # Boutons
        button_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.confirm)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirm(self):
        """Confirme les paramètres."""
        self.settings_confirmed.emit({
            'angle_step': self.angle_spinbox.value(),
            'power_step': self.power_spinbox.value()
        })
        self.accept()

