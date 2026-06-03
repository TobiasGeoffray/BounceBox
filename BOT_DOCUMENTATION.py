"""
📋 DOCUMENTATION DU SYSTÈME DE BOT - BounceBox

Ce document explique comment utiliser le système de Bot IA dans BounceBox.
"""

# Classe Bot (bot.py)
# ====================
#
# Description:
#   La classe Bot implémente une Intelligence Artificielle capable de jouer au BounceBox.
#   Elle utilise un algorithme min-max pour trouver le meilleur coup possible.
#
# Caractéristiques:
#   - Teste tous les angles (pas de 5°, soit 72 angles)
#   - Teste toutes les puissances (pas de 10%, soit 10 puissances)
#   - Total: 720 coups évalués par calcul
#   - Simule chaque coup pour calculer son score
#   - Système de scoring intelligent basé sur le type de boule touchée


# SYSTÈME DE SCORING
# ==================
#
# Le bot évalue chaque coup selon ce système de scoring:
#
#   • Boule grise: 1 point par boule
#   • Boule de couleur adverse: 2 points
#   • Boule de sa propre couleur: 3 points
#   • Aucune boule: 0 point
#
# Le bot choisit le coup avec le score le plus élevé.


# UTILISATION
# ===========
#
# 1. CRÉER UNE PARTIE CONTRE LE BOT
# ----------------------------------
#
#    from partie import Partie
#
#    # Créer une partie avec le Bot comme joueur 2 (Bleu)
#    partie = Partie(
#        nom_joueur1="Vous",      # Joueur humain (Rouge)
#        nom_joueur2="Bot IA",    # Joueur bot (Bleu)
#        points_pour_gagner=5,
#        avec_bot=True            # ← Activer le bot
#    )
#
#    # Démarrer la partie
#    partie.demarrer_partie()


# 2. FAIRE JOUER LE BOT
# --------------------
#
#    # Dans votre boucle de jeu, vérifier si c'est le tour du bot
#    if partie.joueur_actif.est_bot:
#        # Le bot calcule son meilleur coup
#        angle, force = partie.joueur_actif.bot.calculer_meilleur_coup(partie.plateau)
#
#        # Lancer la boule avec cet angle et cette force
#        partie.lancer_boule_blanche(angle, force)


# 3. EXEMPLE COMPLET
# -----------------
#
#    from partie import Partie, EtatPartie
#
#    # Créer et démarrer une partie
#    partie = Partie(nom_joueur1="Alice", nom_joueur2="Bot", avec_bot=True)
#    partie.demarrer_partie()
#
#    # Jouer quelques coups
#    for _ in range(10):
#        if partie.etat == EtatPartie.FIN:
#            break
#
#        if partie.joueur_actif.est_bot:
#            # Bot joue
#            print(f"{partie.joueur_actif.nom} réfléchit...")
#            angle, force = partie.joueur_actif.bot.calculer_meilleur_coup(partie.plateau)
#            partie.lancer_boule_blanche(angle, force)
#        else:
#            # Joueur humain joue (exemple: coup aléatoire)
#            import random
#            angle = random.uniform(0, 360)
#            force = random.uniform(5, 20)
#            partie.lancer_boule_blanche(angle, force)
#
#        # Simuler jusqu'au prochain tour
#        while partie.etat != EtatPartie.TOUR and partie.etat != EtatPartie.FIN:
#            partie.mettre_a_jour_simulation(0.016)


# MODIFICATION DES PARAMÈTRES DU BOT
# ==================================
#
# Vous pouvez modifier la difficulté du bot en changeant les pas:
#
#    # Créer un bot avec des pas plus petits = plus fort (plus lent)
#    bot = Bot(CouleurBoule.BLEUE)
#    bot.pas_angle = 2        # Tester chaque 2° au lieu de 5°
#    bot.pas_puissance = 5    # Tester chaque 5% au lieu de 10%
#
#    # Cela multipliera le temps de calcul!
#    # Angles: 360/2 = 180
#    # Puissances: 100/5 = 20
#    # Total: 180 * 20 = 3600 coups (vs 720 par défaut)


# PERFORMANCE
# ==========
#
# Temps de calcul typique:
#    - Configuration par défaut (720 coups): ~10-15 secondes
#    - Cela dépend de:
#      * Nombre de boules restantes
#      * Configuration de la machine
#      * Nombre d'itérations de simulation
#
# Optimisations possibles:
#    - Augmenter les pas d'angle/puissance pour accélérer
#    - Limiter le nombre de boules à évaluer
#    - Utiliser un algorithme alpha-beta pruning
#    - Évaluer en parallèle les coups


# TESTS
# ====
#
# Fichier de test: test_bot.py
# Lance les tests:     python test_bot.py
#
# Fichier de démo: demo_bot.py
# Lance la démo:       python demo_bot.py


# IMPLÉMENTATION INTERNE
# ======================
#
# Fichiers modifiés/créés:
#
#  1. bot.py (nouveau)
#     - Classe Bot avec algorithme min-max
#     - Méthodes pour calculer et évaluer les coups
#     - Système de scoring
#
#  2. joueur.py (modifié)
#     - Ajout d'un flag "est_bot"
#     - Création automatique d'une instance Bot si nécessaire
#
#  3. partie.py (modifié)
#     - Paramètre "avec_bot" dans __init__
#     - Méthode "executer_coup_bot()" pour le jeu automatisé
#
#  4. test_bot.py (nouveau)
#     - Tests du bot
#     - Test du système de scoring
#
#  5. demo_bot.py (nouveau)
#     - Démonstration interactive du bot


# EXEMPLE D'USAGE EN INTERFACE GRAPHIQUE
# ======================================
#
# Si vous intégrez le bot dans votre interface PyQt6 (main_window.py):
#
#    class MainWindow:
#        def lancer_coup_si_bot(self):
#            \"\"\"Appelé à chaque gicle graphique si c'est le tour du bot.\"\"\"
#            if self.partie.joueur_actif.est_bot and self.partie.etat == EtatPartie.TOUR:
#                angle, force = self.partie.joueur_actif.bot.calculer_meilleur_coup(
#                    self.partie.plateau
#                )
#                self.partie.lancer_boule_blanche(angle, force)


# ALGORITHME MIN-MAX EXPLIQUÉ
# ===========================
#
# Le bot utilise une approche de brute-force min-max:
#
# 1. Pour CHAQUE combinaison possible d'angle et puissance:
#
#    a. SIMULER le coup
#       - Placer la boule blanche avec l'angle et la force
#       - Mettre à jour la simulation jusqu'au repos
#       - Enregistrer toutes les collisions
#
#    b. SCORER le coup
#       - 1 point par boule grise touchée
#       - 2 points par boule adverse touchée
#       - 3 points par boule de la couleur du joueur touchée
#
#    c. NOTER le score associé à ce coup
#
# 2. Retourner le coup avec le MEILLEUR SCORE
#
# C'est appelle min-max car on maximise notre score (max) mais on pourrait
# aussi avoir une version qui minimise le score de l'adversaire.


# AMÉLIORATIONS FUTURES
# =====================
#
# Idées pour rendre le bot encore plus intelligent:
#
#  1. Alpha-Beta Pruning
#     - Évaluer l'ordre des coups pour limiter les branches à explorer
#     - Diviserait drastiquement le temps de calcul
#
#  2. Look-ahead sur plusieurs coups
#     - Prévoir les coupsde l'adversaire
#     - Jouer de manière stratégique
#
#  3. Apprentissage par renforcement
#     - Entraîner le bot sur plusieurs parties
#     - Ajuster les poids du scoring
#
#  4. Endgame tablebase
#     - Pré-calculer les meilleures positions finales
#
#  5. Heuristique pour accélérer
#     - Si beaucoup proche, jouer plus rapidement
#     - Pas de calcul complet nécessaire pour chaque coup


print("✅ Documentation du Bot BounceBox chargée!")

