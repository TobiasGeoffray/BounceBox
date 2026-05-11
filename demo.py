"""
Démonstration du moteur de jeu BounceBox - Étape 1
Ce script teste et démontre toutes les classes du moteur.
"""

from boule import Boule, Boule_blanche, Boule_de_couleur, CouleurBoule
from plateau import Plateau
from joueur import Joueur
from partie import Partie
from trajectoire import Trajectoire


def demo_boules():
    """Démontre les fonctionnalités des boules."""
    print("=" * 50)
    print("DÉMO 1 : Les Boules")
    print("=" * 50)

    # Créer des boules
    boule1 = Boule_blanche(100, 100, vx=10, vy=0)
    boule2 = Boule_de_couleur(120, 100, CouleurBoule.GRISE)

    print(f"Boule 1 : {boule1}")
    print(f"Boule 2 : {boule2}")

    # Test déplacement
    boule1.deplacer(1.0)
    print(f"Après déplacement: {boule1}")

    # Test collision
    if boule1.entre_en_collision_avec(boule2):
        print("✓ Les boules sont en collision !")

    # Test changement de couleur
    boule2.changer_couleur(CouleurBoule.ROUGE)
    print(f"Boule 2 après changement : {boule2}")

    print()


def demo_plateau():
    """Démontre les fonctionnalités du plateau."""
    print("=" * 50)
    print("DÉMO 2 : Le Plateau")
    print("=" * 50)

    # Créer un plateau
    plateau = Plateau(800, 600)
    print(f"Plateau créé : {plateau}")

    # Ajouter des boules
    boule_blanche = Boule_blanche(400, 300, rayon=10)
    boule_grise = Boule_de_couleur(500, 300, CouleurBoule.GRISE, vx=5, vy=0)
    plateau.ajouter_boule(boule_blanche)
    plateau.ajouter_boule(boule_grise)

    print(f"Boules ajoutées : {len(plateau.boules)}")
    print(f"Boule blanche trouvée : {plateau.obtenir_boule_blanche()}")

    # Simulation simple
    print("\nSimulation de 2 secondes...")
    for i in range(125):  # ~2 secondes à 60 FPS
        plateau.mettre_a_jour(0.016)

    print(f"Position boule grise après 2s : ({boule_grise.x:.1f}, {boule_grise.y:.1f})")
    print(f"Vitesse boule grise : ({boule_grise.vx:.2f}, {boule_grise.vy:.2f})")

    print()


def demo_joueurs():
    """Démontre les fonctionnalités des joueurs."""
    print("=" * 50)
    print("DÉMO 3 : Les Joueurs")
    print("=" * 50)

    joueur1 = Joueur("Alice", CouleurBoule.ROUGE)
    joueur2 = Joueur("Bob", CouleurBoule.BLEUE)

    print(f"Joueur 1 : {joueur1}")
    print(f"Joueur 2 : {joueur2}")

    # Ajouter des points
    joueur1.ajouter_point()
    joueur1.ajouter_point()
    joueur1.ajouter_point()

    print(f"\nAprès 3 boules gagnées par Alice : {joueur1}")
    print(f"Alice a gagné ? {joueur1.a_gagne(5)}")

    # Test timer
    print(f"\nTemps restant pour Alice : {joueur1.obtenir_temps_restant():.1f}s")
    joueur1.diminuer_timer(40)
    print(f"Après 40s : {joueur1.obtenir_temps_restant():.1f}s")
    print(f"Temps écoulé ? {joueur1.le_temps_est_ecoule()}")

    print()


def demo_partie():
    """Démontre le moteur de partie."""
    print("=" * 50)
    print("DÉMO 4 : Une Partie Complète")
    print("=" * 50)

    partie = Partie("Alice", "Bob", points_pour_gagner=5)
    partie.demarrer_partie()

    print(f"Partie créée : {partie}")
    print(f"État : {partie.obtenir_etat_partie()}")

    # Simulation : Alice lance la boule blanche
    print("\n--- Alice lance la boule blanche ---")
    print("Angle: 45°, Force: 100")

    try:
        partie.lancer_boule_blanche(angle_degres=45, force=100)

        # Simuler quelques frames
        for frame in range(100):  # ~1.6 secondes
            partie.mettre_a_jour_simulation(0.016)

        print(f"\nAprès simulation :")
        print(f"État de la partie : {partie.obtenir_etat_partie()}")
        print(f"Boules gagnées ce tour : {len(partie.boules_gagnees_ce_tour)}")

    except RuntimeError as e:
        print(f"Erreur : {e}")

    print()


def demo_trajectoire():
    """Démontre les trajectoires."""
    print("=" * 50)
    print("DÉMO 5 : Les Trajectoires")
    print("=" * 50)

    boule = Boule_blanche(100, 100, vx=30, vy=40)
    trajectoire = Trajectoire(boule, enregistrer_historique=True)

    print(f"Boule : {boule}")
    print(f"Vitesse : {trajectoire.obtenir_vitesse_actuelle():.2f} px/s")
    print(f"Angle : {trajectoire.obtenir_angle_actuel():.1f}°")

    # Simuler le mouvement
    print("\nSimulation de trajectoire...")
    for i in range(100):
        boule.deplacer(0.016)
        boule.appliquer_resistance(0.99)
        trajectoire.enregistrer_position()

    print(f"Distance parcourue estimée : {trajectoire.predire_distance_parcourue():.1f} px")
    print(f"Positions enregistrées : {len(trajectoire.obtenir_historique())}")
    print(f"Position finale : ({boule.x:.1f}, {boule.y:.1f})")

    print()


def main():
    """Lance toutes les démos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║    DÉMONSTRATION DU MOTEUR BOUNCEBOX - ÉTAPE 1        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()

    try:
        demo_boules()
        demo_plateau()
        demo_joueurs()
        demo_trajectoire()
        demo_partie()

        print("=" * 50)
        print("✅ TOUTES LES DÉMOS COMPLÉTÉES AVEC SUCCÈS !")
        print("=" * 50)
        print("\nPour exécuter les tests unitaires :")
        print("  python -m unittest test_bouncebox -v")
        print()

    except Exception as e:
        print(f"❌ Erreur pendant la démo : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

