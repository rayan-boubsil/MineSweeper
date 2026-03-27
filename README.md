
```markdown
# 🚩 Minesweeper - Matrix Edition

Un jeu de Démineur moderne développé en **Python** avec la bibliothèque **Pygame**. Cette version propose une esthétique "Terminal/Matrix" et une architecture découplée (MVC) pour une performance et une lisibilité optimales.

## 🚀 Fonctionnalités

- **Trois niveaux de difficulté** : Débutant, Intermédiaire et Expert.
- **Génération intelligente** : La première case cliquée n'est jamais une mine.
- **Difficulté dynamique** : Nombre de mines aléatoire dans une plage définie pour chaque niveau.
- **Système de Pause** : Interrompez votre partie à tout moment avec `P` ou `Echap`.
- **Sauvegarde du score** : Enregistrement des meilleurs temps avec le nom du joueur.
- **Interface Matrix** : Design néon vert et noir avec animations au survol des boutons.

## 🛠️ Installation

1. Assurez-vous d'avoir Python 3.x installé.
2. Installez la bibliothèque Pygame :
   ```bash
   pip install pygame
   ```
3. Lancez le jeu :
   ```bash
   python main.py
   ```

## 🎮 Commandes en jeu

| Touche | Action |
| :--- | :--- |
| **Clic Gauche** | Révéler une case |
| **Clic Droit** | Placer/Retirer un drapeau |
| **R** | Réinitialiser la partie (Restart) |
| **P / Echap** | Mettre en pause / Reprendre |
| **Q** | Retourner au Menu Principal |

---

## 🎵 Personnalisation : Sons et Musiques

Le projet est configuré pour supporter une ambiance sonore immersive. Pour ajouter vos propres fichiers, placez-les dans l'arborescence suivante :

### 📂 Emplacement des fichiers
À la racine de votre projet, créez ou utilisez le dossier `assets/` :

1. **Effets sonores (SFX)** :
   - Chemin : `assets/sounds/`
   - Fichiers attendus : `click.wav`, `explosion.wav`, `flag.wav`, `win.wav`.
2. **Musique de fond (BGM)** :
   - Chemin : `assets/music/`
   - Fichier attendu : `background_matrix.mp3` (ou tout autre format supporté par Pygame).

> **Note** : Si vous changez les noms des fichiers, pensez à mettre à jour les chemins dans votre classe `AudioEngine` ou vos constantes.

---

## 📐 Architecture du projet

Le projet suit une structure modulaire :
- `main.py` : Point d'entrée de l'application.
- `core/` : Logique pure du jeu (Grille, algorithmes de révélation).
- `display/` : Gestion de l'affichage et du rendu Pygame (Renderer).
- `ui/` : Éléments d'interface réutilisables (Boutons, Inputs).
- `data/` : Sauvegardes des scores et états de jeu.
