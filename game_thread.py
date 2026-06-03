"""
GameThread : Gère la boucle de jeu dans un thread séparé.
Exécute la simulation du moteur BounceBox et émet des signaux Qt.
"""

import time
from PyQt5.QtCore import QThread, pyqtSignal
from partie import Partie, EtatPartie
from boule import CouleurBoule


class GameThread(QThread):
    """
    Thread de jeu qui gère la simulation du moteur BounceBox.
    Émet des signaux pour mettre à jour l'interface graphique.

    Signaux:
        - board_update : Les données du plateau ont changé, redessiner
        - scores_update : Les scores ont changé
        - timer_update : Le timer a changé
        - player_changed : Le joueur actif a changé
        - game_over : La partie est terminée
        - ball_launched : Une boule a été lancée
    """

    # Signaux
    board_update = pyqtSignal()  # Redessiner le plateau
    scores_update = pyqtSignal(dict)  # Nouveau score
    timer_update = pyqtSignal(float)  # Temps restant
    player_changed = pyqtSignal(str, str)  # Nom joueur, couleur
    game_over = pyqtSignal(str, int, int)  # Gagnant, score1, score2
    ball_launched = pyqtSignal()  # Boule lancée

    def __init__(self, joueur1_nom="Joueur 1", joueur2_nom="Joueur 2",
                 points_pour_gagner=5, avec_bot=False):
        """
        Initialise le thread de jeu.

        Args:
            joueur1_nom (str): Nom du joueur 1 (rouge)
            joueur2_nom (str): Nom du joueur 2 (bleu)
            points_pour_gagner (int): Points pour gagner (par défaut 5)
            avec_bot (bool): True pour jouer contre le bot, False pour 2 joueurs (par défaut False)
        """
        super().__init__()
        self.partie = Partie(joueur1_nom, joueur2_nom,
                            points_pour_gagner=points_pour_gagner,
                            avec_bot=avec_bot)
        self.is_running = False
        self.is_paused = False
        self.fps_target = 60
        self.dt = 1.0 / self.fps_target
        self.current_angle = 0
        self.current_force = 0
        self.bot_played = False  # Flag pour éviter de faire jouer le bot plusieurs fois

    def run(self):
        """
        Boucle principale du jeu (exécutée dans le thread).
        """
        self.is_running = True
        self.partie.demarrer_partie()

        # Émettre l'état initial
        self._emit_initial_state()

        clock = time.time()

        while self.is_running:
            if not self.is_paused:
                # Timing du jeu
                current_time = time.time()
                elapsed = current_time - clock
                clock += self.dt

                # Vérifier timeout
                self._check_timeout()

                # Mettre à jour la simulation
                self.partie.mettre_a_jour_simulation(self.dt)

                # Faire jouer le bot si c'est son tour
                self._bot_play_if_needed()

                # Émettre les signaux
                self._emit_updates()

                # Vérifier fin de partie
                if self.partie.etat == EtatPartie.FIN:
                    self._emit_game_over()
                    self.is_running = False
                    break

            # Attendre pour obtenir ~60 FPS
            sleep_time = self.dt - (time.time() - clock)
            if sleep_time > 0:
                time.sleep(sleep_time / 1000.0)

    def _emit_initial_state(self):
        """Émet l'état initial du jeu après démarrage."""
        self.scores_update.emit({
            'joueur1': self.partie.joueur1.nom,
            'score1': self.partie.joueur1.score,
            'joueur2': self.partie.joueur2.nom,
            'score2': self.partie.joueur2.score,
        })

        joueur = self.partie.joueur_actif
        couleur_str = "🔴 ROUGE" if joueur.couleur == CouleurBoule.ROUGE else "🔵 BLEU"
        self.player_changed.emit(joueur.nom, couleur_str)
        self.timer_update.emit(joueur.obtenir_temps_restant())
        self.board_update.emit()

    def _emit_updates(self):
        """Émet les signaux de mise à jour."""
        # Mise à jour du plateau (redessiner)
        self.board_update.emit()

        # Mise à jour du timer
        self.timer_update.emit(self.partie.joueur_actif.obtenir_temps_restant())

        # Mise à jour des scores
        self.scores_update.emit({
            'joueur1': self.partie.joueur1.nom,
            'score1': self.partie.joueur1.score,
            'joueur2': self.partie.joueur2.nom,
            'score2': self.partie.joueur2.score,
        })

    def _check_timeout(self):
        """Vérifie si le temps du tour est écoulé."""
        joueur_actif = self.partie.joueur_actif
        joueur_actif.diminuer_timer(self.dt)

        if joueur_actif.le_temps_est_ecoule() and self.partie.etat == EtatPartie.TOUR:
            # Le joueur n'a pas lancé à temps
            print(f"⏱️  {joueur_actif.nom} a dépassé le délai imparti !")
            self.partie.finir_tour()
            self._emit_player_changed()
            self.bot_played = False  # Réinitialiser pour le nouveau tour

    def _bot_play_if_needed(self):
        """
        Fait jouer le bot automatiquement si c'est son tour.
        Cette méthode est appelée à chaque frame.
        """
        if (not self.partie.joueur_actif.est_bot and
                self.bot_played):
            self.bot_played = False

        elif (self.partie.joueur_actif.est_bot and
            not self.bot_played):
            
            print(f"🤖 {self.partie.joueur_actif.nom} est en train de calculer...")
            
            # Calculer et jouer le meilleur coup
            angle, force = self.partie.joueur_actif.bot.calculer_meilleur_coup(self.partie.plateau)
            
            print(f"🤖 {self.partie.joueur_actif.nom} joue: angle={angle:.0f}°, force={force:.1f}")
            
            # Lancer la boule
            self.lancer_boule_blanche(angle, force)
            
            # Marquer que le bot a joué
            self.bot_played = True

    def _emit_player_changed(self):
        """Émet le signal de changement de joueur."""
        joueur = self.partie.joueur_actif
        couleur_str = "🔴 ROUGE" if joueur.couleur == CouleurBoule.ROUGE else "🔵 BLEU"
        
        # Réinitialiser le flag du bot quand le joueur change
        self.bot_played = False

        self.player_changed.emit(joueur.nom, couleur_str)

    def _emit_game_over(self):
        """Émet le signal de fin de partie."""
        gagnant = self.partie.joueur1 if self.partie.joueur1.a_gagne(5) else self.partie.joueur2
        self.game_over.emit(
            gagnant.nom,
            self.partie.joueur1.score,
            self.partie.joueur2.score
        )

    def lancer_boule_blanche(self, angle_degres, force):
        """
        Lance la boule blanche.

        Args:
            angle_degres (float): Angle en degrés
            force (float): Force du lancement (0-100)
        """
        if self.partie.etat == EtatPartie.TOUR:
            try:
                self.partie.lancer_boule_blanche(angle_degres, force)
                self.ball_launched.emit()
                print(f"🎯 Boule lancée : angle={angle_degres:.1f}°, force={force:.1f}")
            except RuntimeError as e:
                print(f"❌ Erreur : {e}")

    def restart_game(self):
        """Redémarre une nouvelle partie."""
        self.is_running = False
        self.wait()  # Attendre que le thread se termine
        self.partie = Partie(self.partie.joueur1.nom, self.partie.joueur2.nom)
        self.start()

    def pause_game(self):
        """Met le jeu en pause."""
        self.is_paused = True

    def resume_game(self):
        """Reprend le jeu."""
        self.is_paused = False

    def stop_game(self):
        """Arrête le jeu."""
        self.is_running = False

    def get_plateau(self):
        """Retourne le plateau de la partie actuelle."""
        return self.partie.plateau

    def get_partie(self):
        """Retourne la partie actuelle."""
        return self.partie

