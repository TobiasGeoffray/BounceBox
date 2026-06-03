"""Démonstration du bot joueur dans le jeu BounceBox."""

from partie import Partie, EtatPartie
import time


def demo_contre_bot():
    """
    Démontre une partie contre le bot.

    Le bot utilise un algorithme min-max pour calculer le meilleur coup.
    Il teste tous les angles (pas de 5°) et puissances (pas de 10%)
    et évalue chaque coup selon le système de scoring suivant:
    - 1 point par boule grise touchée
    - 2 points: boule adverse touchée
    - 3 points: boule de la couleur du joueur touchée
    """
    print("=" * 60)
    print("DEMO - BounceBox avec BOT")
    print("=" * 60)
    print()

    # Créer une partie contre le bot
    print("Création d'une partie contre le bot...")
    partie = Partie(
        nom_joueur1="Joueur Humain",
        nom_joueur2="Bot IA",
        points_pour_gagner=3,
        avec_bot=True
    )

    print(f"Joueur 1: {partie.joueur1.nom} (ROUGE) - Humain")
    print(f"Joueur 2: {partie.joueur2.nom} (BLEU) - Bot IA")
    print(f"Points pour gagner: {partie.points_pour_gagner}")
    print()

    # Démarrer la partie
    print("Démarrage de la partie...")
    partie.demarrer_partie()
    print(f"Nombre de boules: {len(partie.plateau.boules)}")
    print()

    # Simuler quelques tours
    tour_count = 0
    max_tours = 10

    while partie.etat != EtatPartie.FIN and tour_count < max_tours:
        tour_count += 1

        print(f"\n--- TOUR {tour_count} ---")
        print(f"Joueur actif: {partie.joueur_actif.nom} ({partie.joueur_actif.couleur.value})")
        print(f"Score: {partie.joueur1.nom} {partie.joueur1.score} - {partie.joueur2.nom} {partie.joueur2.score}")

        # Si c'est le tour du bot, il joue automatiquement
        if partie.joueur_actif.est_bot:
            print(f"\n{partie.joueur_actif.nom} calcule son meilleur coup...")
            print("(En cours d'analyse de tous les angles et puissances possibles...)")

            # Calculer le meilleur coup
            angle, force = partie.joueur_actif.bot.calculer_meilleur_coup(partie.plateau)

            print(f"Meilleur coup trouvé:")
            print(f"  - Angle: {angle}°")
            print(f"  - Force: {force} (soit {force/10 * 10:.0f}% de puissance)")
            print()

            partie.lancer_boule_blanche(angle, force)
        else:
            # Coup aléatoire pour le joueur humain (simulation)
            import random
            import math

            angle = random.uniform(0, 360)
            force = random.uniform(5, 20)

            print(f"\n{partie.joueur_actif.nom} joue:")
            print(f"  - Angle: {angle:.1f}°")
            print(f"  - Force: {force:.1f}")
            print()

            partie.lancer_boule_blanche(angle, force)

        # Simuler le coup jusqu'à ce que les boules s'arrêtent
        iterations = 0
        while partie.etat == EtatPartie.ATTENTE and iterations < 5000:
            partie.mettre_a_jour_simulation(0.016)
            iterations += 1

        # Afficher les résultats du tour
        if partie.boules_gagnees_ce_tour:
            print(f"Boules gagnées ce tour: {len(partie.boules_gagnees_ce_tour)}")
            for boule in partie.boules_gagnees_ce_tour:
                print(f"  - {boule.couleur.value}")
        else:
            print("Aucune boule gagnée ce tour")

        # Finir le tour
        partie.finir_tour()

    # Afficher le résultat final
    print("\n" + "=" * 60)
    if partie.etat == EtatPartie.FIN:
        gagnant = partie.joueur_actif
        print(f"FIN DE PARTIE!")
        print(f"Gagnant: {gagnant.nom} ({gagnant.couleur.value})")
        print(f"Score final: {partie.joueur1.nom} {partie.joueur1.score} - {partie.joueur2.nom} {partie.joueur2.score}")
    else:
        print("Démonstration terminée (limite de tours atteinte)")

    print("=" * 60)
    print()


def demo_bot_vs_bot():
    """Démontre une partie Bot vs Bot (2 bots qui jouent ensemble)."""
    print("\n" + "=" * 60)
    print("DEMO - BOT vs BOT")
    print("=" * 60)
    print()

    # Note: Pour avoir 2 bots, il faudrait modifier Partie
    # Pour l'instant, cette fonction affiche juste comment faire
    print("Note: Pour faire jouer 2 bots ensemble, vous pouvez modifier la classe Partie")
    print("pour accepter un paramètre 'joueur1_est_bot' en plus de 'avec_bot'.")
    print()


if __name__ == "__main__":
    print("\n" + "🤖 DÉMONSTRATION DU BOT BOUNCEBOX 🤖\n")

    # Demo 1: Joueur contre Bot
    demo_contre_bot()

    # Demo 2: Info sur Bot vs Bot
    demo_bot_vs_bot()

    print("\n✅ Démonstrations terminées!")

