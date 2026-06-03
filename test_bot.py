"""Test rapide du bot - sans simulation complète."""

from partie import Partie, EtatPartie
from boule import CouleurBoule
import time


def test_bot_calcul_coup():
    """Test que le bot peut calculer un coup rapidement."""
    print("=" * 60)
    print("TEST - Calcul du meilleur coup par le Bot")
    print("=" * 60)
    print()

    # Créer une partie contre le bot
    partie = Partie(
        nom_joueur1="Joueur Humain",
        nom_joueur2="Bot IA",
        avec_bot=True
    )

    # Démarrer la partie
    partie.demarrer_partie()

    print(f"Joueur 1: {partie.joueur1.nom} ({partie.joueur1.couleur.value})")
    print(f"Joueur 2: {partie.joueur2.nom} ({partie.joueur2.couleur.value})")
    print(f"Est bot: {partie.joueur2.est_bot}")
    print()

    # Premier coup du joueur humain
    print("Tour 1: Joueur Humain joue")
    partie.lancer_boule_blanche(45, 10)

    # Simuler jusqu'à arrêt - mettre_a_jour_simulation appelle finir_tour automatiquement
    for _ in range(1000):
        partie.mettre_a_jour_simulation(0.016)
        if partie.etat == EtatPartie.TOUR:  # Vérifier si on est passé au tour suivant
            break

    print("OK - Boules arrêtées et passage au tour suivant")
    print()

    # Maintenant c'est le tour du Bot
    print("Tour 2: Bot calcule son meilleur coup...")
    print(f"Boules restantes: {len(partie.plateau.boules)}")
    print(f"Joueur actif: {partie.joueur_actif.nom} ({partie.joueur_actif.couleur.value})")
    print(f"Est bot: {partie.joueur_actif.est_bot}")
    print()

    if partie.joueur_actif.est_bot:
        print("Lancement du calcul min-max du bot...")
        print("(Cela peut prendre quelques secondes...)")
        print()

        start_time = time.time()
        angle, force = partie.joueur_actif.bot.calculer_meilleur_coup(partie.plateau)
        elapsed = time.time() - start_time

        print(f"✅ Calcul terminé en {elapsed:.2f} secondes")
        print()
        print(f"Meilleur coup trouvé par le bot:")
        print(f"  - Angle: {angle:.1f}°")
        print(f"  - Force: {force:.1f}")
        print(f"  - Puissance: {force/10*10:.0f}%")
        print()

        # Paramètres du bot
        print(f"Pas d'angle du bot: {partie.joueur_actif.bot.pas_angle}°")
        print(f"Pas de puissance du bot: {partie.joueur_actif.bot.pas_puissance}%")
        total_coups = (360 // partie.joueur_actif.bot.pas_angle) * (100 // partie.joueur_actif.bot.pas_puissance)
        print(f"Nombre total de coups évalués: {total_coups}")
        print()

        print("✅ TEST RÉUSSI - Le bot fonctionne correctement!")
    else:
        print("❌ ERREUR - Ce n'est pas le tour du bot")


def test_scoring():
    """Test le système de scoring du bot."""
    print()
    print("=" * 60)
    print("TEST - Système de Scoring du Bot")
    print("=" * 60)
    print()

    from boule import Boule_de_couleur, Boule_blanche
    from bot import Bot

    bot = Bot(CouleurBoule.ROUGE)

    # Test avec chaque couleur
    boule_grise = Boule_de_couleur(100, 100, CouleurBoule.GRISE)
    boule_rouge = Boule_de_couleur(100, 100, CouleurBoule.ROUGE)
    boule_bleue = Boule_de_couleur(100, 100, CouleurBoule.BLEUE)

    print("Bot couleur: ROUGE")
    print()
    print(f"Score pour boule grise: {bot._scorer_collision(boule_grise)} (attendu: 1)")
    print(f"Score pour boule rouge (couleur du bot): {bot._scorer_collision(boule_rouge)} (attendu: 3)")
    print(f"Score pour boule bleue (adverse): {bot._scorer_collision(boule_bleue)} (attendu: 2)")
    print()

    all_correct = (
        bot._scorer_collision(boule_grise) == 1 and
        bot._scorer_collision(boule_rouge) == 3 and
        bot._scorer_collision(boule_bleue) == 2
    )

    if all_correct:
        print("✅ TEST RÉUSSI - Le scoring est correct!")
    else:
        print("❌ ERREUR - Le scoring est incorrect")


if __name__ == "__main__":
    print("\n" + "🤖 TESTS DU BOT BOUNCEBOX 🤖\n")

    test_scoring()
    test_bot_calcul_coup()

    print("\n" + "=" * 60)
    print("✅ Tous les tests sont terminés!")
    print("=" * 60)

