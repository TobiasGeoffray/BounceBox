# 🎮 GUIDE D'UTILISATION - INTERFACE GRAPHIQUE AVEC BOT

## 🚀 Lancer le Jeu

```bash
python main.py
```

La fenêtre s'ouvrira et vous affichera l'écran de sélection du mode de jeu.

---

## 🎯 Écran 1: Sélection du Mode de Jeu

Vous verrez un dialogue avec deux options:

### Option 1: **2 Joueurs Humains** ✅ (Par défaut)
- Deux joueurs jouent l'un après l'autre
- Joueur 1 (Rouge) commence
- Joueur 2 (Bleu) joue après
- Chacun a 45 secondes par tour

**Pour utiliser:**
1. Laissez la sélection par défaut
2. Modifiez les noms si souhaité
3. Réglez les points pour gagner
4. Cliquez "Démarrer la Partie"

### Option 2: **Jouer contre le Bot IA** 🤖
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
- 5° = Normal (60 angles × 10 puissances = 720 coups testés)
- 2° = Difficile (180 angles × 10 puissances = 1800 coups testés)
- 1° = Expert (360 angles × 10 puissances = 3600 coups testés)

**Précision de la puissance (par défaut: 10%)**
- Plus petit = Plus difficile
- 10% = Normal (10, 20, 30...100%)
- 5% = Difficile (5, 10, 15...100%)
- 1% = Expert (1, 2, 3...100%)

### Temps d'attente:
- Normal (5°, 10%): 10-15 secondes
- Difficile (2°, 10%): 30-50 secondes
- Expert (1°, 1%): 5+ minutes

**Conseil:** Commencez en Normal (5°, 10%)!

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

| Type de boule | Points gagnés |
|---|---|
| Boule grise | 1 point |
| Boule adverse | 2 points |
| Boule propre | 3 points |
| Aucune boule | 0 point |

**Exemple:**
- Alice (rouge) tire et touche: 1 grise, 1 rouge = 1 + 3 = 4 points ✅
- Bob (bleu) tire et touche: 1 bleue = 3 points ✅

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
   - Préfère ses boules (3 pts)
   - Évite les contacts dangereux

2. **Il est prévisible** - Le bot ne regarde que le coup actuel
   - Il n'anticipe pas vos prochains coups
   - Vous pouvez utiliser ça à votre avantage!

3. **L'attente est normale** - Le bot prend 10-15 secondes
   - C'est le temps de calculer 720 coups
   - Soyez patient! ☕

4. **Vous CAN gagner** - Le bot n'est pas parfait
   - Vous avez aussi 45 secondes
   - Vous pouvez prendre un temps pour réfléchir
   - La chance existe aussi!

---

## ⌨️ Raccourcis

- **Nouvelle Partie** - Bouton "Nouvelle Partie"
- **Quitter** - Bouton "Quitter" ou Fermer la fenêtre
- **Viser** - Cliquer et glisser sur la boule blanche

---

## ❓ FAQ

**Q: Pourquoi le bot met du temps?**
A: Il teste 720 coups différents (72 angles × 10 puissances). C'est le temps normal.

**Q: Le bot peut-il tricher?**
A: Non! Il utilise exactement le même système que vous (même physique, même scoring).

**Q: On peut jouer Bot vs Bot?**
A: Pas actuellement. Vous êtes toujours le Joueur 1. À développer!

**Q: Comment battre le bot?**
A: Le bot est très bon au jeu. Bonne chance! 😄

**Q: Le bot peut-il s'améliorer?**
A: Oui! Les développeurs peuvent ajouter:
- Look-ahead (prévoir plusieurs coups)
- Apprentissage par renforcement
- Alpha-beta pruning (calcul plus rapide)

**Q: Pourquoi le bot est toujours bleu?**
A: Parce que le Joueur 1 (rouge) commence, et les humains aiment commencer. À modifier si souhaité!

---

## 🐛 Dépannage

### La souris ne répond pas?
- Vous êtes peut-être en attendant le bot
- Attendez que le bot finisse son coup

### La boule ne lance pas?
- Cliquez directement sur la boule blanche (rayon ~50 pixels)
- Glissez suffisamment loin (minimum 5 pixels)

### Le jeu fige pendant 10-15 secondes?
- C'est NORMAL si c'est le tour du bot
- Le bot calcule les 720 meilleurs coups
- Attendez qu'il finisse

### L'interface est lente?
- Fermez d'autres applications
- Réduisez la précision du bot (augmentez les pas d'angle/puissance)

---

## 📈 Modifie les Noms des Joueurs

sur l'écran de sélection du mode:
1. Cliquez dans le champ "Joueur 1 (ROUGE)"
2. Tapez votre nom
3. Même chose pour Joueur 2 (si 2 joueurs humains)

---

## 🎮 Comments Fonctionne le Gameplay

### Joueur Humain:
```
Frame 1: Vous cliquez sur la boule
         ↓
Frame 2-100: Vous glissez (guide visuel)
             ↓
Frame 101: Vous relâchez
           ↓
Frame 102-500: Simulation (boules en mouvement)
               ↓
Frame 501: Tour terminé
           ↓
Frame 502: C'est le tour du bot / autre joueur
```

### Bot:
```
Frame 1: C'est le tour du bot
         ↓
Frame 2-3000: Bot calcule (10-15 secondes)
              ↓
Frame 3001: Bot lance la boule
            ↓
Frame 3002-3500: Simulation (boules en mouvement)
                 ↓
Frame 3501: Tour terminé
            ↓
Frame 3502: C'est votre tour / autre joueur
```

---

## 🚀 Améliorations Futures

- [ ] Bot vs Bot (2 bots qui jouent ensemble)
- [ ] Configuration du bot en jeu (pas besoin de redémarrer)
- [ ] Statistiques de partie
- [ ] Sauvegarde des parties
- [ ] Multijoueur en réseau
- [ ] Sons et musique
- [ ] Skins/Thèmes

---

**Amusez-vous bien! 🎮🤖**

