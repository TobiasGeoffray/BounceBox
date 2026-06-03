"""
Exemple d'utilisation complète du système de Bot dans l'interface graphique.

Ce fichier montre comment l'interface graphique utilise le bot IA.
"""

# FLUX DE DÉMARRAGE DE L'APPLICATION:
# ===================================
#
# 1. main.py démarre l'appli PyQt5
#    └─> QApplication créée
#    └─> MainWindow créée


# 2. MainWindow.__init__() :
#    └─> show_game_mode_dialog() appelé


# 3. GameModeDialog affichée :
#    ┌─ Utilisateur sélectionne le mode
#    └─ Signal "game_started" émis avec les paramètres


# 4. MainWindow.on_game_mode_selected(params) :
#    ├─ Si avec_bot=True: afficher SettingsDialog
#    └─ Sinon: start_game() directement


# 5. MainWindow.start_game(params, bot_settings) :
#    ├─ Créer GameThread avec les paramètres
#    ├─ Configurer le bot si nécessaire:
#    │  └─ gamethread.partie.joueur2.bot.pas_angle = settings['angle_step']
#    │  └─ gamethread.partie.joueur2.bot.pas_puissance = settings['power_step']
#    └─ Appeler setup_ui() pour afficher le plateau


# 6. GameThread.run() - Boucle principale :
#    ├─ À chaque frame (~60 FPS):
#    │  ├─ partie.mettre_a_jour_simulation(dt)
#    │  ├─ _bot_play_if_needed()  ← LE MAGIC!
#    │  └─ émetteur des signaux pour mise à jour GUI
#    └─ game_over vérifié


# 7. GameThread._bot_play_if_needed() :
#    ├─ Vérifie si c'est le tour du bot
#    ├─ Calcule le meilleur coup:
#    │  └─ angle, force = bot.calculer_meilleur_coup(plateau)
#    ├─ Lance la boule:
#    │  └─ lancer_boule_blanche(angle, force)
#    └─ Marque bot_played = True pour éviter relance


# 8. GameWidget affiche le plateau :
#    ├─ Si c'est le tour du bot: afficher "🤖 Bot réfléchit..."
#    ├─ Si joueur humain: afficher le guide de visée
#    └─ Accepte clics souris UNIQUEMENT pour joueur humain


# ARCHITECTURE:
# =============
#
#                       main.py
#                          |
#                    MainWindow
#                       /    \
#                      /      \
#             GameModeDialog  GameThread
#                              /    \
#                             /      \
#                        Partie      GameWidget
#                           |
#                    (joueur1, joueur2)
#                                     \
#                                      Bot IA
#                                   (min-max)


# INTERACTION AVEC LE BOT:
# ========================
#
# JOUEUR HUMAIN:
#    1. Clique sur la boule blanche
#    2. Glisse pour viser → guide visuel
#    3. Relâche → lancer_boule_blanche() signal
#    4. Boules en mouvement → simulation
#    5. Quand terminé → tour suivant
#
# BOT IA:
#    1. GameThread détecte que c'est le tour du bot
#    2. _bot_play_if_needed() est appelé
#    3. Bot calcule tous les coups (720 évaluations)
#    4. Retourne le meilleur coup
#    5. Lance automatiquement la boule
#    6. Simulation continue
#    7. Quand terminé → tour suivant


# EXEMPLE DE FLUX COMPLET:
# =========================
#
# Partie humain (Alice) vs Bot
#
# Frame 1-100:  Alice joue son coup
# Frame 101:    tour = Alice → tour = Bot
# Frame 102-1200: Bot calcule (10-15 sec) ~720 évaluations de coups
# Frame 1201:   Bot trouve le meilleur coup et le joue
# Frame 1202-1500: Boules en mouvement du coup du bot
# Frame 1501:   Toutes les boules arrêtées
# Frame 1502:   tour = Bot → tour = Alice
# ...
# Répétition jusqu'à victoire


# MODIFICATIONS POUR SUPPORTER LE BOT:
# ====================================
#
# game_thread.py:
#    ✅ __init__: ajout paramètre avec_bot
#    ✅ _bot_play_if_needed(): fait jouer le bot
#    ✅ bot_played flag: évite double lancement
#
# game_widget.py:
#    ✅ mousePressEvent(): vérifie si c'est le tour du bot
#    ✅ paintEvent(): affiche "Bot réfléchit..." si bot
#
# main_window.py:
#    ✅ show_game_mode_dialog(): écran de sélection
#    ✅ on_game_mode_selected(): dialogue paramètres bot
#    ✅ start_game(): crée partie avec/sans bot
#    ✅ new_game(): redémarre avec nouveau choix
#
# joueur.py:
#    ✅ est_bot flag: marque si joueur est bot
#    ✅ bot instance: crée Bot si est_bot=True
#
# partie.py:
#    ✅ __init__: paramètre avec_bot
#


# NOTES IMPORTANTES:
# ==================
#
# 1. Le bot joue LENTEMENT (10-15 sec) car il teste 720 coups
#    → C'est normal! Pour accélérer: diminuer les pas d'angle/puissance
#
# 2. Le bot est toujours Joueur 2 (bleu)
#    → À modifier si vous voulez bot vs bot ou bot j1
#
# 3. L'interface est bloquée pendant le calcul du bot
#    → À améliorer avec threading ou async si trop lent
#
# 4. Le bot évalue toujours la MEILLEURE position actuellement
#    → Il n'anticipe pas les coups futurs
#    → À améliorer avec look-ahead


print("✅ Ce fichier explique l'intégration du Bot IA dans l'interface graphique!")

