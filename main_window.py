"""
MainWindow : Fenêtre principale de l'application Qt (Version Fusionnée et Corrigée).
Résout le problème d'interface blanche en limitant la portée de la feuille de style.
"""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from game_thread import GameThread
from game_widget import GameWidget
from game_mode_dialog import GameModeDialog, SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BounceBox - Jeu de Billard")
        self.setObjectName("MainWindow")  # Nécessaire pour cibler précisément la fenêtre en CSS
        self.setMinimumSize(1180, 820)
        self.setStyleSheet("QMainWindow#MainWindow { background-color: #fffdf0; }")
        self.game_thread = None
        self.game_widget = None
        self.bot_settings = {'angle_step': 5, 'power_step': 10}
        # Afficher le dialogue de sélection de mode
        self.show_game_mode_dialog()

    def show_game_mode_dialog(self):
        """Affiche le dialogue de sélection du mode de jeu."""
        dialog = GameModeDialog(self)
        dialog.game_started.connect(self.on_game_mode_selected)
        dialog.exec_()

    def on_game_mode_selected(self, params):
        """Appelé quand l'utilisateur a sélectionné un mode de jeu."""
        if params['with_bot']:
            settings_dialog = SettingsDialog(self)
            settings_dialog.settings_confirmed.connect(
                lambda s: self.start_game(params, s)
            )
            settings_dialog.exec_()
        else:
            self.start_game(params, self.bot_settings)

    def start_game(self, params, bot_settings=None):
        """Démarre une partie avec les paramètres donnés."""
        if bot_settings:
            self.bot_settings = bot_settings

        self.game_thread = GameThread(
            params['player1_name'],
            params['player2_name'],
            points_pour_gagner=params['points_to_win'],
            avec_bot=params['with_bot']
        )

        if params['with_bot'] and self.game_thread.partie.joueur2.est_bot:
            self.game_thread.partie.joueur2.bot.pas_angle = self.bot_settings['angle_step']
            self.game_thread.partie.joueur2.bot.pas_puissance = self.bot_settings['power_step']

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur modernisée avec bandeau supérieur centré."""
        main_widget = QWidget()
        layout_principal_vertical = QVBoxLayout(main_widget)
        layout_principal_vertical.setContentsMargins(30, 20, 30, 20)
        layout_principal_vertical.setSpacing(20)

        # =========================================================================
        # 1. BANDEAU SUPÉRIEUR (HEADER ENCADRÉ ET CENTRÉ)
        # =========================================================================
        cadre_titre = QFrame()
        cadre_titre.setObjectName("HeaderFrame")
        cadre_titre.setStyleSheet("""
            QFrame#HeaderFrame {
                background-color: #e8e6d5;
                border: 2px solid #c7c5b5;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        layout_titre = QVBoxLayout(cadre_titre)
        layout_titre.setAlignment(Qt.AlignCenter)  # Tout aligner au centre à l'intérieur
        layout_titre.setSpacing(4)
        lbl_nom_jeu = QLabel("BOUNCE BOX")
        lbl_nom_jeu.setFont(QFont("Segoe UI", 26, QFont.Bold))
        lbl_nom_jeu.setStyleSheet("color: #000000; letter-spacing: 3px; background: transparent;")
        lbl_nom_jeu.setAlignment(Qt.AlignCenter)
        layout_titre.addWidget(lbl_nom_jeu)
        lbl_credits = QLabel("Projet Informatique Fise 28 — Tobias Geoffray et Ugo Royer")
        lbl_credits.setFont(QFont("Segoe UI", 11, QFont.Medium))
        lbl_credits.setStyleSheet("color: #000000; background: transparent;")
        lbl_credits.setAlignment(Qt.AlignCenter)
        layout_titre.addWidget(lbl_credits)

        # Ajout du bandeau tout en haut du layout principal
        layout_principal_vertical.addWidget(cadre_titre)
        layout_contenu_horizontal = QHBoxLayout()
        layout_contenu_horizontal.setSpacing(30)
        # --- ZONE DE JEU (GAUCHE / CENTRÉ) ---
        layout_jeu_vertical = QVBoxLayout()
        layout_jeu_vertical.setAlignment(Qt.AlignCenter)

        self.game_widget = GameWidget(self.game_thread)
        self.game_widget.setFixedSize(850, 630)

        layout_jeu_vertical.addWidget(self.game_widget)
        layout_contenu_horizontal.addLayout(layout_jeu_vertical, stretch=4)

        # --- PANNEAU LATÉRAL (DROITE) ---
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)

        # Cadre des statistiques de jeu
        self.cadre_score = QFrame()
        self.cadre_score.setObjectName("Scoreboard")
        self.cadre_score.setStyleSheet("""
            QFrame#Scoreboard {
                background-color: #e8e6d5;
                border: 2px solid #c7c5b5;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                color: #000000;
                background: transparent;
            }
        """)

        layout_cadre = QVBoxLayout(self.cadre_score)
        layout_cadre.setSpacing(12)

        # Label Joueur Actif
        self.label_player = QLabel("Joueur: Joueur 1")
        self.label_player.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout_cadre.addWidget(self.label_player)

        # Séparateur
        ligne_sep = QFrame()
        ligne_sep.setFrameShape(QFrame.HLine)
        ligne_sep.setStyleSheet("background-color: #c7c5b5;")
        layout_cadre.addWidget(ligne_sep)

        # Labels Scores
        self.label_score1 = QLabel("Joueur 1: 0")
        self.label_score1.setFont(QFont("Segoe UI", 11))
        layout_cadre.addWidget(self.label_score1)

        self.label_score2 = QLabel("Joueur 2: 0")
        self.label_score2.setFont(QFont("Segoe UI", 11))
        layout_cadre.addWidget(self.label_score2)

        # Label Chronomètre
        self.label_timer = QLabel("Temps: 45s")
        self.label_timer.setFont(QFont("Consolas", 14, QFont.Bold))
        self.label_timer.setStyleSheet("color: #000000; background-color: #d6d4c3; border-radius: 6px; padding: 6px;")
        self.label_timer.setAlignment(Qt.AlignCenter)
        layout_cadre.addWidget(self.label_timer)

        right_layout.addWidget(self.cadre_score)
        right_layout.addSpacing(25)

        # Boutons d'actions
        style_boutons = """
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QPushButton:pressed {
                background-color: #005999;
            }
            QPushButton#BtnQuitter {
                background-color: #d9534f;
            }
            QPushButton#BtnQuitter:hover {
                background-color: #c9302c;
            }
        """

        btn_new = QPushButton("🔄 Nouvelle Partie")
        btn_new.setStyleSheet(style_boutons)
        btn_new.clicked.connect(self.new_game)
        right_layout.addWidget(btn_new)

        right_layout.addSpacing(10)

        btn_quit = QPushButton("❌ Quitter")
        btn_quit.setObjectName("BtnQuitter")
        btn_quit.setStyleSheet(style_boutons)
        btn_quit.clicked.connect(self.quit_game)
        right_layout.addWidget(btn_quit)

        right_layout.addStretch()
        layout_contenu_horizontal.addLayout(right_layout, stretch=1)

        # Assemblage final du layout horizontal sous le header
        layout_principal_vertical.addLayout(layout_contenu_horizontal)

        self.setCentralWidget(main_widget)

        # Connecter les signaux
        self.game_thread.scores_update.connect(self.on_scores_update)
        self.game_thread.player_changed.connect(self.on_player_changed)
        self.game_thread.timer_update.connect(self.on_timer_update)
        self.game_thread.game_over.connect(self.on_game_over)
        self.game_widget.ball_launch_requested.connect(self.on_ball_launch)

        # Démarrer le jeu
        self.game_thread.start()

    def on_ball_launch(self, angle, force):
        if self.game_thread:
            self.game_thread.lancer_boule_blanche(angle, force)

    def on_scores_update(self, scores):
        self.label_score1.setText(f"🔴 {scores['joueur1']} : {scores['score1']} pts")
        self.label_score2.setText(f"🔵 {scores['joueur2']} : {scores['score2']} pts")

    def on_player_changed(self, nom, couleur):
        print(f"DEBUG: Mise à jour UI pour {nom}")
        print(f"DEBUG: Signal reçu -> Nom: '{nom}', Couleur: '{couleur}'")
        # 1. Mise à jour du texte
        self.label_player.setText(f"🎯 Tour : {nom}")
        self.label_player.repaint()
        # 2. Définition de la couleur de bordure
        couleur_str = str(couleur).upper()
        if "ROUGE" in couleur_str:
            border_color = "#ff4444"
        elif "BLEU" in couleur_str:
            border_color = "#33a3ff"
        else:
            border_color = "#c7c5b5"

        # 3. Application du style directement sur l'objet
        # On ajoute 'qproperty-objectName' pour forcer la reconnaissance du sélecteur CSS
        style = f"""
            QFrame#Scoreboard {{
                background-color: #e8e6d5;
                border: 3px solid {border_color};
                border-radius: 15px;
                padding: 15px;
            }}
        """
        self.cadre_score.setStyleSheet("background-color: white")

        # 4. LE SECRET POUR QT :
        # Si le cadre est dans un layout, il faut forcer le layout à se redessiner
        self.cadre_score.update()
        self.cadre_score.parentWidget().update()  # Redessine aussi le conteneur


    def on_timer_update(self, temps):
        self.label_timer.setText(f"⏱️ Temps restant : {temps:.1f}s")

    def on_game_over(self, gagnant, score1, score2):
        msg = f"🎉 {gagnant} a gagné!\n{score1} - {score2}"
        QMessageBox.information(self, "Partie Terminée", msg)

    def new_game(self):
        if self.game_thread:
            self.game_thread.stop_game()
            self.game_thread.wait()
        self.setCentralWidget(QWidget())
        self.show_game_mode_dialog()

    def quit_game(self):
        self.close()

    def closeEvent(self, event):
        print("🛑 Fermeture de l'application détectée...")

        if self.game_thread and hasattr(self.game_thread, 'partie') and self.game_thread.partie:
            try:
                print("💾 Lancement de la sauvegarde des statistiques...")
                self.game_thread.partie.sauvegarder_statistiques()
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde automatique : {e}")

        if self.game_thread:
            self.game_thread.stop_game()
            if self.game_thread.isRunning():
                self.game_thread.is_running = False
                self.game_thread.wait()

        event.accept()