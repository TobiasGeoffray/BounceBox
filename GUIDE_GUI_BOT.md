# 🎮 GUIDE D'UTILISATION - INTERFACE GRAPHIQUE AVEC BOT

## 🚀 Lancer le Jeu

```bash
python main.py
```

La fenêtre s'ouvrira et vous affichera l'écran de sélection du mode de jeu.

---

## 🎯 Écran 1 : Sélection du Mode de Jeu

Vous verrez un dialogue avec deux options:

### Option 1 : **2 Joueurs Humains** ✅ (Par défaut)
- Deux joueurs jouent l'un après l'autre
- Joueur 1 (Rouge) commence
- Joueur 2 (Bleu) joue après
- Chacun a 45 secondes par tour

**Pour utiliser:**
1. Laissez la sélection par défaut
2. Modifiez les noms si souhaité
3. Réglez les points pour gagner
4. Cliquez "Démarrer la Partie"

### Option 2 : **Jouer contre le Bot IA** 🤖
- Vous êtes Joueur 1 (Rouge)
- Le Bot IA est Joueur 2 (Bleu)
- Le bot joue automatiquement après vous

**Pour utiliser:**
1. Sélectionnez "Jouer contre le Bot IA"
2. Remarquez que le nom "Joueur 2" devient "Bot IA" (grisé)
3. Réglez les points pour gagner
4. Cliquez "Démarrer la Partie"

---

## ⚙️ Écran 2: Paramètres du Bot (Si vous avez choisi le bot)

### Difficultés disponibles:

**Précision des angles (par défaut: 5°)**
- Plus petit = Plus difficile
- 10° = Normal (36 angles)
- 5° = Difficile (72 angles)
- 2° = Expert (180 angles) ⚠️Temps de calcul long⚠️

**Précision de la puissance (par défaut: 10%)**
- Plus petit = Plus difficile
- 50% = Normal (50, 100, 150...300%)
- 10% = Difficile (10, 20, 30...300%)

### Temps d'attente:
- Normal (10°, 50%): 5 secondes
- Difficile (5°, 10%): 30-50 secondes
- Expert (2°, 10%): +2 minutes

**Conseil:** Commencez en Normal (10°, 50%)!

---

## 🎮 Écran 3: Plateau de Jeu

### Pour les Joueurs Humains:

1. **Attendez votre tour** - L'écran affiche "Joueur: [Votre nom]"

2. **Visez** - Cliquez sur la boule blanche et maintenez

3. **Tirez** - Glissez avec la souris
   - Distance = Force
   - Angle = Position de la souris
   - Vous verrez "Angle: XX° | Force: XX%"

4. **Relâchez** - La boule se lance

5. **Regardez** - Les boules se déplacent et collisionnent

6. **Fin du tour** - Quand toutes les boules s'arrêtent, c'est le tour de l'autre

### Pour le Bot:

1. **Il réfléchit** - Vous verrez "🤖 Bot IA réfléchit..."
   - Le bot calcule les 720 meilleurs coups possibles

2. **Il joue** - Le bot tire automatiquement

3. **Les boules bougent** - Exactement comme un joueur humain

4. **Fin de son tour** - Après l'arrêt des boules, c'est votre tour

### Affichage:
- **Score** - Affichage du score de chaque joueur
- **Temps** - Temps restant pour jouer (45 secondes)
- **Joueur actif** - Qui joue en ce moment
- **Boules** - 1 blanche (vous) + 9 grises + 2 de chaque couleur

---

## 📊 Système de Scoring

À chaque coup, le joueur/bot essaie de marquer des points:
Pour marquer un point il faut "coloré" une boule en la touchant avec la blanche, puis lorsqu'elle est de votre couleur retouchez la pour gagner un point.


**Exemple:**
- Alice (rouge) tire et touche: 1 grise, 1 rouge => elle colore la grise et gagne un point avec la rouge
- Bob (bleu) tire et touche: 1 bleue => il gagne un point

---

## 🏆 Fin de Partie

Quand un joueur atteint le nombre de points requis:

1. Une fenêtre apparaît: "🎉 [Gagnant] a gagné! XX - YY"
2. Vous pouvez:
   - **Nouvelle Partie** - Retour à l'écran de sélection
   - **Quitter** - Fermer l'application

---

## 💡 Conseils de Jeu

### Contre le Bot:

1. **Il est intelligent** - Le bot choisit toujours le meilleur coup
   - Touche les boules si possible
   - Préfère ses boules 
   - Évite les contacts dangereux

2. **Il est prévisible** - Le bot ne regarde que le coup actuel
   - Il n'anticipe pas vos prochains coups
   - Vous pouvez utiliser ça à votre avantage!

3. **L'attente est normale** - Le bot prend 10-15 secondes
   - C'est le temps de calculer 300 coups
   - Soyez patient! ☕

4. **Vous pouvez gagner** - Le bot n'est pas parfait (loin de la)
   - Vous avez aussi 45 secondes
   - Vous pouvez prendre un temps pour réfléchir
   - La chance existe aussi!

---
**Amusez-vous bien! 🎮🤖**

