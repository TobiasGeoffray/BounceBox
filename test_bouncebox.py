"""Tests unitaires pour les classes du jeu BounceBox."""

import unittest
import math
from boule import Boule, Boule_blanche, Boule_de_couleur, CouleurBoule
from plateau import Plateau
from joueur import Joueur
from impact import Impact
from partie import Partie, EtatPartie
from trajectoire import Trajectoire


class TestBoule(unittest.TestCase):
    """Tests pour la classe Boule."""

    def test_creation_boule(self):
        """Test la création d'une boule."""
        boule = Boule_blanche(100, 200)
        self.assertEqual(boule.x, 100)
        self.assertEqual(boule.y, 200)
        self.assertEqual(boule.couleur, CouleurBoule.BLANCHE)
        self.assertEqual(boule.rayon, 10)

    def test_deplacer_boule(self):
        """Test le déplacement d'une boule."""
        boule = Boule_de_couleur(100, 100, CouleurBoule.ROUGE, vx=10, vy=20)
        boule.deplacer(1.0)
        self.assertEqual(boule.x, 110)
        self.assertEqual(boule.y, 120)

    def test_arreter_boule(self):
        """Test l'arrêt d'une boule."""
        boule = Boule_blanche(100, 100, vx=10, vy=20)
        boule.arreter()
        self.assertEqual(boule.vx, 0)
        self.assertEqual(boule.vy, 0)

    def test_est_arretee(self):
        """Test la détection d'une boule arrêtée."""
        boule_en_mouvement = Boule_blanche(100, 100, vx=10, vy=0)
        self.assertFalse(boule_en_mouvement.est_arrêtee())

        boule_arretee = Boule_blanche(100, 100, vx=0, vy=0)
        self.assertTrue(boule_arretee.est_arrêtee())

    def test_changer_couleur(self):
        """Test le changement de couleur."""
        boule = Boule_de_couleur(100, 100, CouleurBoule.GRISE)
        boule.changer_couleur(CouleurBoule.ROUGE)
        self.assertEqual(boule.couleur, CouleurBoule.ROUGE)

    def test_distance_entre_boules(self):
        """Test le calcul de distance entre deux boules."""
        boule1 = Boule_blanche(0, 0)
        boule2 = Boule_de_couleur(3, 4, CouleurBoule.GRISE)
        distance = boule1.distance_vers(boule2)
        self.assertAlmostEqual(distance, 5.0)

    def test_collision_entre_boules(self):
        """Test la détection de collision."""
        boule1 = Boule_blanche(0, 0, rayon=10)
        boule2 = Boule_de_couleur(15, 0, CouleurBoule.GRISE, rayon=10)
        self.assertTrue(boule1.entre_en_collision_avec(boule2))

        boule3 = Boule_de_couleur(100, 0, CouleurBoule.GRISE, rayon=10)
        self.assertFalse(boule1.entre_en_collision_avec(boule3))


class TestPlateau(unittest.TestCase):
    """Tests pour la classe Plateau."""

    def test_creation_plateau(self):
        """Test la création d'un plateau."""
        plateau = Plateau(800, 600)
        self.assertEqual(plateau.largeur, 800)
        self.assertEqual(plateau.hauteur, 600)
        self.assertEqual(len(plateau.boules), 0)

    def test_ajouter_boule(self):
        """Test l'ajout d'une boule."""
        plateau = Plateau()
        boule = Boule_blanche(400, 300)
        plateau.ajouter_boule(boule)
        self.assertEqual(len(plateau.boules), 1)

    def test_retirer_boule(self):
        """Test le retrait d'une boule."""
        plateau = Plateau()
        boule = Boule_blanche(400, 300)
        plateau.ajouter_boule(boule)
        plateau.retirer_boule(boule)
        self.assertEqual(len(plateau.boules), 0)

    def test_obtenir_boules_par_couleur(self):
        """Test la récupération de boules par couleur."""
        plateau = Plateau()
        boule1 = Boule_de_couleur(100, 100, CouleurBoule.ROUGE)
        boule2 = Boule_de_couleur(200, 200, CouleurBoule.ROUGE)
        boule3 = Boule_de_couleur(300, 300, CouleurBoule.GRISE)
        plateau.ajouter_boule(boule1)
        plateau.ajouter_boule(boule2)
        plateau.ajouter_boule(boule3)

        boules_rouges = plateau.obtenir_boules_par_couleur(CouleurBoule.ROUGE)
        self.assertEqual(len(boules_rouges), 2)

    def test_rebond_bordure_gauche(self):
        """Test le rebond sur la bordure gauche."""
        plateau = Plateau(800, 600)
        boule = Boule_blanche(5, 300, rayon=10, vx=-20, vy=0)
        plateau.ajouter_boule(boule)
        plateau.gerer_rebond_bordures()
        self.assertGreater(boule.vx, 0)  # La vitesse x doit être positive après rebond

    def test_rebond_bordure_droite(self):
        """Test le rebond sur la bordure droite."""
        plateau = Plateau(800, 600)
        boule = Boule_blanche(795, 300, rayon=10, vx=20, vy=0)
        plateau.ajouter_boule(boule)
        plateau.gerer_rebond_bordures()
        self.assertLess(boule.vx, 0)  # La vitesse x doit être négative après rebond


class TestJoueur(unittest.TestCase):
    """Tests pour la classe Joueur."""

    def test_creation_joueur(self):
        """Test la création d'un joueur."""
        joueur = Joueur("Alice", CouleurBoule.ROUGE)
        self.assertEqual(joueur.nom, "Alice")
        self.assertEqual(joueur.couleur, CouleurBoule.ROUGE)
        self.assertEqual(joueur.score, 0)

    def test_ajouter_point(self):
        """Test l'ajout de points."""
        joueur = Joueur("Bob", CouleurBoule.BLEUE)
        joueur.ajouter_point()
        self.assertEqual(joueur.score, 1)
        joueur.ajouter_point()
        self.assertEqual(joueur.score, 2)

    def test_a_gagne(self):
        """Test la vérification de victoire."""
        joueur = Joueur("Charlie", CouleurBoule.ROUGE)
        self.assertFalse(joueur.a_gagne(5))

        for _ in range(5):
            joueur.ajouter_point()
        self.assertTrue(joueur.a_gagne(5))

    def test_timer(self):
        """Test le timer du tour."""
        joueur = Joueur("Dave", CouleurBoule.BLEUE, temps_limite_tour=10)
        self.assertEqual(joueur.temps_restant, 10)

        joueur.diminuer_timer(3)
        self.assertEqual(joueur.temps_restant, 7)

        self.assertFalse(joueur.le_temps_est_ecoule())
        joueur.diminuer_timer(7.1)
        self.assertTrue(joueur.le_temps_est_ecoule())


class TestImpact(unittest.TestCase):
    """Tests pour la classe Impact."""

    def test_detecter_collision(self):
        """Test la détection de collision."""
        boule1 = Boule_blanche(0, 0, rayon=10)
        boule2 = Boule_de_couleur(15, 0, CouleurBoule.GRISE, rayon=10)
        self.assertTrue(Impact.detecter_collision(boule1, boule2))

    def test_appliquer_regle_couleur_grise(self):
        """Test l'application de la règle avec boule grise."""
        boule_blanche = Boule_blanche(0, 0)
        boule_grise = Boule_de_couleur(20, 0, CouleurBoule.GRISE)

        resultat = Impact.appliquer_regle_couleur(boule_blanche, boule_grise, CouleurBoule.ROUGE)
        self.assertEqual(resultat, "gris")
        self.assertEqual(boule_grise.couleur, CouleurBoule.ROUGE)

    def test_appliquer_regle_couleur_gagnee(self):
        """Test l'application de la règle avec boule gagnée."""
        boule_blanche = Boule_blanche(0, 0)
        boule_rouge = Boule_de_couleur(20, 0, CouleurBoule.ROUGE)

        resultat = Impact.appliquer_regle_couleur(boule_blanche, boule_rouge, CouleurBoule.ROUGE)
        self.assertEqual(resultat, "gagne")

    def test_appliquer_regle_couleur_adverse(self):
        """Test l'application de la règle avec boule adverse."""
        boule_blanche = Boule_blanche(0, 0)
        boule_bleue = Boule_de_couleur(20, 0, CouleurBoule.BLEUE)

        resultat = Impact.appliquer_regle_couleur(boule_blanche, boule_bleue, CouleurBoule.ROUGE)
        self.assertEqual(resultat, "adverse_grise")
        self.assertEqual(boule_bleue.couleur, CouleurBoule.GRISE)


class TestPartie(unittest.TestCase):
    """Tests pour la classe Partie."""

    def test_creation_partie(self):
        """Test la création d'une partie."""
        partie = Partie("Alice", "Bob")
        self.assertEqual(partie.joueur1.nom, "Alice")
        self.assertEqual(partie.joueur2.nom, "Bob")
        self.assertEqual(partie.etat, EtatPartie.DEBUT)

    def test_demarrer_partie(self):
        """Test le démarrage d'une partie."""
        partie = Partie()
        partie.demarrer_partie()
        self.assertEqual(partie.etat, EtatPartie.TOUR)
        # 1 blanche + 9 grises + 2 bleues = 12 boules
        self.assertEqual(len(partie.plateau.boules), 12)

    def test_joueur_rouge_commence(self):
        """Test que le joueur rouge commence."""
        partie = Partie()
        partie.demarrer_partie()
        self.assertEqual(partie.joueur_actif.couleur, CouleurBoule.ROUGE)


class TestTrajectoire(unittest.TestCase):
    """Tests pour la classe Trajectoire."""

    def test_creation_trajectoire(self):
        """Test la création d'une trajectoire."""
        boule = Boule_blanche(100, 100, vx=10, vy=0)
        traj = Trajectoire(boule)
        self.assertEqual(traj.boule, boule)

    def test_obtenir_angle_actuel(self):
        """Test le calcul de l'angle."""
        boule = Boule_blanche(100, 100, vx=10, vy=0)
        traj = Trajectoire(boule)
        angle = traj.obtenir_angle_actuel()
        self.assertAlmostEqual(angle, 0, delta=1)  # Environ 0°

    def test_obtenir_vitesse_actuelle(self):
        """Test le calcul de la vitesse."""
        boule = Boule_blanche(100, 100, vx=3, vy=4)
        traj = Trajectoire(boule)
        vitesse = traj.obtenir_vitesse_actuelle()
        self.assertAlmostEqual(vitesse, 5.0)


if __name__ == '__main__':
    unittest.main()

