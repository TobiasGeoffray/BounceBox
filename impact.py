"""Classe pour gérer les impacts et collisions entre boules."""

from math import sqrt
from boule import Boule, CouleurBoule


class Impact:
    """
    Gère la détection et la résolution des collisions entre boules.
    """

    @staticmethod
    def detecter_collision(boule1: Boule, boule2: Boule) -> bool:
        """
        Détecte une collision entre deux boules.

        Args:
            boule1 (Boule): Première boule
            boule2 (Boule): Deuxième boule

        Returns:
            bool: True si les boules entrent en collision
        """
        return boule1.entre_en_collision_avec(boule2)

    @staticmethod
    def resoudre_collision_elastique(boule1: Boule, boule2: Boule):
        """
        Résout une collision élastique entre deux boules.
        Échange les vitesses normales selon les masses.

        Args:
            boule1 (Boule): Première boule
            boule2 (Boule): Deuxième boule
        """
        # Vecteur entre les centres des boules
        dx = boule2.x - boule1.x
        dy = boule2.y - boule1.y
        distance = sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return  # Les boules sont au même endroit, on évite une division par zéro

        # Normaliser le vecteur
        nx = dx / distance
        ny = dy / distance

        # Vitesses relatives
        dvx = boule2.vx - boule1.vx
        dvy = boule2.vy - boule1.vy

        # Vitesse relative selon la normale
        dvn = dvx * nx + dvy * ny

        # Ne traiter que si les boules se rapprochent
        if dvn >= 0:
            return

        # Calcul de l'impulsion (pour un coefficient de restitution de 1)
        # Avec masses égales m1 = m2 = m : impulsion = -dvn / 2
        impulsion = -dvn / (boule1.masse + boule2.masse)

        # Appliquer l'impulsion
        boule1.vx -= impulsion * boule1.masse * nx
        boule1.vy -= impulsion * boule1.masse * ny
        boule2.vx += impulsion * boule2.masse * nx
        boule2.vy += impulsion * boule2.masse * ny

        # Séparer les boules pour éviter qu'elles se chevauchent
        chevauchement = boule1.rayon + boule2.rayon - distance
        if chevauchement > 0:
            separation = chevauchement / 2 + 0.01
            boule1.x -= separation * nx
            boule1.y -= separation * ny
            boule2.x += separation * nx
            boule2.y += separation * ny

    @staticmethod
    def appliquer_regle_couleur(boule_blanche: Boule, boule_touchee: Boule, couleur_joueur: CouleurBoule):
        """
        Applique la règle de changement de couleur suite à une collision.

        Règles:
        - Si la boule est grise, elle prend la couleur du joueur
        - Si la boule est de la couleur du joueur, elle est gagnée (à retirer)
        - Si la boule est de la couleur adverse, elle redevient grise

        Args:
            boule_blanche (Boule): La boule blanche
            boule_touchee (Boule): La boule touchée
            couleur_joueur (CouleurBoule): La couleur du joueur qui lance

        Returns:
            str: Un des "gris", "gagne", "adverse_grise" ou "aucun"
        """
        if boule_touchee.couleur == CouleurBoule.GRISE:
            boule_touchee.changer_couleur(couleur_joueur)
            return "gris"
        elif boule_touchee.couleur == couleur_joueur:
            # La boule est gagnée (elle sera retirée du plateau)
            return "gagne"
        elif boule_touchee.couleur in [CouleurBoule.ROUGE, CouleurBoule.BLEUE]:
            # Il s'agit d'une boule adverse
            boule_touchee.changer_couleur(CouleurBoule.GRISE)
            return "adverse_grise"

        return "aucun"

    @staticmethod
    def detecter_et_resoudre_collisions_boules(boules) -> list:
        """
        Détecte et résout toutes les collisions entre boules.
        Retourne une liste des impacts (collisions avec la boule blanche).

        Args:
            boules (List[Boule]): Liste de toutes les boules

        Returns:
            list: Liste des tuples (boule_blanche, boule_touchee) pour les collisions
        """
        collisions = []
        boule_blanche = next((b for b in boules if b.couleur == CouleurBoule.BLANCHE), None)

        if not boule_blanche:
            return collisions

        # Vérifier les collisions avec la boule blanche
        for boule in boules:
            if boule != boule_blanche:
                if Impact.detecter_collision(boule_blanche, boule):
                    collisions.append((boule_blanche, boule))
                    Impact.resoudre_collision_elastique(boule_blanche, boule)

        # Vérifier les collisions entre autres boules
        for i in range(len(boules)):
            for j in range(i + 1, len(boules)):
                if boules[i].couleur != CouleurBoule.BLANCHE and boules[j].couleur != CouleurBoule.BLANCHE:
                    if Impact.detecter_collision(boules[i], boules[j]):
                        Impact.resoudre_collision_elastique(boules[i], boules[j])

        return collisions

    @staticmethod
    def __repr__(self):
        """Représentation textuelle de l'impact."""
        return "Impact(gestionnaire de collisions)"

