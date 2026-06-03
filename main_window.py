"""MainWindow : Fenêtre principale de l'application Qt (Version Fusionnée)."""
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from game_thread import GameThread
from game_widget import GameWidget
from game_mode_dialog import GameModeDialog, SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BounceBox - Jeu de Billard")
        self.setGeometry(100, 100, 1024, 700)
        self.game_thread = None
        self.game_widget = None
        self.bot_settings = {'angle_step': 5, 'power_step': 10}

        # Afficher le dialogue de sélection de mode (Ajout binôme)
        self.show_game_mode_dialog()

    def show_game_mode_dialog(self):
        """Affiche le dialogue de sélection du mode de jeu."""
        dialog = GameModeDialog(self)
        dialog.game_started.connect(self.on_game_mode_selected)
        dialog.exec_()

    def on_game_mode_selected(self, params):
        """Appelé quand l'utilisateur a sélectionné un mode de jeu."""
        # Si c'est contre le bot, afficher les paramètres du bot
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

        # Créer le thread de jeu avec les paramètres choisis
        self.game_thread = GameThread(
            params['player1_name'],
            params['player2_name'],
            points_pour_gagner=params['points_to_win'],
            avec_bot=params['with_bot']
        )

        # Configurer les paramètres du bot si nécessaire
        if params['with_bot'] and self.game_thread.partie.joueur2.est_bot:
            self.game_thread.partie.joueur2.bot.pas_angle = self.bot_settings['angle_step']
            self.game_thread.partie.joueur2.bot.pas_puissance = self.bot_settings['power_step']

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur du jeu."""
        main_widget = QWidget()
        layout = QHBoxLayout()

        # Zone de jeu
        self.game_widget = GameWidget(self.game_thread)

        # Panneau droit
        right_layout = QVBoxLayout()

        # Labels
        self.label_player = QLabel("Joueur: Joueur 1")
        self.label_score1 = QLabel("Joueur 1: 0")
        self.label_score2 = QLabel("Joueur 2: 0")
        self.label_timer = QLabel("Temps: 45s")

        # Boutons
        btn_new = QPushButton("Nouvelle Partie")
        btn_new.clicked.connect(self.new_game)

        btn_quit = QPushButton("Quitter")
        btn_quit.clicked.connect(self.quit_game)

        right_layout.addWidget(self.label_player)
        right_layout.addWidget(self.label_score1)
        right_layout.addWidget(self.label_score2)
        right_layout.addWidget(self.label_timer)
        right_layout.addWidget(btn_new)
        right_layout.addWidget(btn_quit)
        right_layout.addStretch()

        layout.addWidget(self.game_widget)
        layout.addLayout(right_layout)
        main_widget.setLayout(layout)
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
        self.label_score1.setText(f"{scores['joueur1']}: {scores['score1']}")
        self.label_score2.setText(f"{scores['joueur2']}: {scores['score2']}")

    def on_player_changed(self, nom, couleur):
        self.label_player.setText(f"Joueur: {nom} {couleur}")

    def on_timer_update(self, temps):
        self.label_timer.setText(f"Temps: {temps:.1f}s")

    def on_game_over(self, gagnant, score1, score2):
        msg = f"🎉 {gagnant} a gagné!\n{score1} - {score2}"
        QMessageBox.information(self, "Partie Terminée", msg)

    def new_game(self):
        """Arrête le match et affiche à nouveau l'accueil des modes de jeu."""
        if self.game_thread:
            self.game_thread.stop_game()
            self.game_thread.wait()
        self.setCentralWidget(QWidget())  # Vider la fenêtre
        self.show_game_mode_dialog()

    def quit_game(self):
        """Action déclenchée lors du clic sur le bouton Quitter."""
        self.close()  # Déclenche automatiquement l'événement closeEvent ci-dessous

    def closeEvent(self, event):
        """
        Méthode UNIQUE et sécurisée de fermeture de l'application (Bouton Quitter ou Croix X).
        Gère la sauvegarde de vos statistiques et l'arrêt propre du moteur.
        """
        print("🛑 Fermeture de l'application détectée...")

        # 💾 Votre système de sauvegarde des statistiques
        if self.game_thread and hasattr(self.game_thread, 'partie') and self.game_thread.partie:
            try:
                print("💾 Lancement de la sauvegarde des statistiques...")
                self.game_thread.partie.sauvegarder_statistiques()
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde automatique : {e}")

        # Arrêt propre du thread de calcul
        if self.game_thread:
            self.game_thread.stop_game()
            if self.game_thread.isRunning():
                self.game_thread.is_running = False
                self.game_thread.wait()

        event.accept()