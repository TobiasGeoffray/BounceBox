# 🎱 BounceBox

Un jeu de billard à deux joueurs simulé en Python, avec physique réaliste et interface graphique.

## 🎮 Principe du jeu

BounceBox oppose deux joueurs — **Rouge** et **Bleu** — sur un plateau rectangulaire. À tour de rôle, chaque joueur vise et lance la **boule blanche** pour toucher les boules colorées.

**Règles de collision :**
- Toucher une boule **grise** → elle prend la couleur du joueur
- Toucher une boule de **sa propre couleur** → elle est marquée et retirée (+1 point)
- Toucher une boule de la **couleur adverse** → elle redevient grise

Le premier joueur à atteindre **5 points** remporte la partie. Chaque tour est limité dans le temps !

## 🚀 Installation

```bash
git clone https://github.com/TobiasGeoffray/BounceBox.git
cd BounceBox
pip install PyQt5
```

## ▶️ Lancer le jeu

```bash
python main.py
```

Vous serez accueilli par un écran de sélection du mode de jeu :
- **2 Joueurs Humains** : Jouez avec une autre personne
- **Jouer contre le Bot IA** : Affrontez une intelligence artificielle

## 🤖 Bot IA

BounceBox propose un **Bot IA intelligent** basé sur un algorithme **min-max optimisé**.

### Comment jouer contre le Bot

1. Lancez le jeu : `python main.py`
2. Sélectionnez **« Jouer contre le Bot IA »**
3. Configurez la **difficulté** (ajustez la précision des angles et puissances)
4. Le Bot joue automatiquement après vous

### Fonctionnement du Bot

Le Bot calcule le **meilleur coup possible** en :
- **Phase 1 (Coarse)** : Teste une grille grossière d'angles et puissances pour identifier les régions prometteuses
- **Phase 2 (Refinement)** : Affine la recherche autour des meilleurs candidats avec la précision complète

**Paramètres ajustables :**
- **Précision des angles** : 5° (normal, ~60 angles), 2° (difficile, ~180 angles), 1° (expert, ~360 angles)
- **Précision de la puissance** : 10% (normal, 10 valeurs), 5% (difficile, 20 valeurs), 1% (expert, 100 valeurs)

**Temps de calcul typique :**
- Normal (5°, 10%) : 2-5 secondes
- Difficile (2°, 10%) : 5-10 secondes
- Expert (1°, 1%) : 30+ secondes

### Système de scoring du Bot

Le Bot évalue chaque coup selon :
- **1 point** : Boule grise touchée
- **2 points** : Boule adverse touchée
- **3 points** : Boule de sa propre couleur touchée

Le Bot choisit le coup qui maximise ce score.

### Architecture de la computation

- Le calcul du Bot s'exécute dans un **processus séparé** pour ne pas bloquer l'interface
- L'interface reste **réactive** pendant le calcul (affichage, timer, vérification de timeout)
- Si le temps imparti s'écoule, le processus du Bot est **terminé automatiquement**

## 🧪 Lancer les tests

```bash
python -m unittest test_bouncebox.py -v
```

## 📁 Structure du projet

| Fichier | Description |
|---|---|
| `main.py` | Point d'entrée du programme |
| `boule.py` | Classe `Boule` et ses variantes (`Boule_blanche`, `Boule_de_couleur`) |
| `plateau.py` | Gestion du plateau de jeu (rebonds, résistance) |
| `joueur.py` | Classe `Joueur` (score, minuteur, support Bot) |
| `partie.py` | Logique complète d'une partie (support mode Bot) |
| `impact.py` | Détection et résolution des collisions élastiques |
| `trajectoire.py` | Suivi et prédiction de trajectoire |
| `bot.py` | **Classe `Bot` avec algorithme min-max optimisé** |
| `game_widget.py` | Interface graphique (Qt) |
| `game_thread.py` | Thread de simulation (support computation asynchrone Bot) |
| `game_mode_dialog.py` | Dialogue de sélection mode de jeu et paramètres Bot |
| `test_bouncebox.py` | Tests unitaires (27 tests) |

## ⚙️ Fonctionnement technique

### Simulation du jeu

La simulation tourne à ~60 FPS. À chaque frame :
1. Les boules se déplacent selon leur vitesse (`vx`, `vy`)
2. Les rebonds sur les bords sont gérés
3. Un coefficient de résistance ralentit progressivement les boules
4. Les collisions élastiques sont détectées et résolues (conservation de la quantité de mouvement)

### Calcul du Bot IA

Le Bot utilise un **algorithme min-max à deux phases** :
- **Phase 1 (Coarse)** : Grille grossière pour localiser les régions prometteuses (rapide)
- **Phase 2 (Refinement)** : Affinage précis autour des meilleurs candidats

La computation s'exécute dans un **processus séparé** (multiprocessing) pour :
- Éviter le blocage de la boucle graphique
- Permettre l'interruption si le temps imparti s'écoule
- Maintenir une interface réactive pendant le calcul

Pour plus de détails téchniques, consultez `BOT_DOCUMENTATION.py` ou `GUIDE_GUI_BOT.md`.

## 🐍 Dépendances

- Python 3.x
- PyQt5 (interface graphique)

## 📚 Documentation supplémentaire

| Document | Contenu |
|---|---|
| `GUIDE_GUI_BOT.md` | Guide complet pour jouer contre le Bot (pour les utilisateurs) |
| `BOT_DOCUMENTATION.py` | Documentation téchnique du Bot IA avec exemples de code |
| `INTEGRATION_BOT_GUI.md` | Architecture et flux d'intégration du Bot dans l'interface graphique |
| `RESUME_GUI_BOT.md` | Résumé des modifications d'intégration du Bot |

## 👤 Auteur

Tobias Geoffray et Ugo Royer — Projet Info 2ème semestre
