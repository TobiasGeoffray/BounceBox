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
| `joueur.py` | Classe `Joueur` (score, minuteur) |
| `partie.py` | Logique complète d'une partie |
| `impact.py` | Détection et résolution des collisions élastiques |
| `trajectoire.py` | Suivi et prédiction de trajectoire |
| `game_widget.py` | Interface graphique (Qt) |
| `game_thread.py` | Thread de simulation |
| `test_bouncebox.py` | Tests unitaires |

## ⚙️ Fonctionnement technique

La simulation tourne à ~60 FPS. À chaque frame :
1. Les boules se déplacent selon leur vitesse (`vx`, `vy`)
2. Les rebonds sur les bords sont gérés
3. Un coefficient de résistance ralentit progressivement les boules
4. Les collisions élastiques sont détectées et résolues (conservation de la quantité de mouvement)

## 🐍 Dépendances

- Python 3.x
- PyQt5 (interface graphique)

## 👤 Auteur

Tobias Geoffray et Ugo Royer — Projet Info 2ème semestre
