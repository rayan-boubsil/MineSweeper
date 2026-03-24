import pygame
import random
from cell import Cell, CELL_SIZE, HEADER_H


class Grid:

    # --- Le constructeur est appelé automatiquement à la création de la grille ---
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows         = rows    # nombre de lignes
        self.cols         = cols    # nombre de colonnes
        self.mines        = mines   # nombre de mines à placer
        self.cells        = []      # contiendra toutes les cases (liste de listes)
        self._initialized = False   # devient True une fois les mines placées (après le 1er clic)
        self._build()               # on construit la grille vide dès la création

    # --- Crée la grille vide : une liste de lignes, chaque ligne contenant des cases ---
    def _build(self):
        # Pour chaque ligne r et chaque colonne c, on crée un objet Cell
        # Résultat : self.cells[r][c] donne la case à la ligne r, colonne c
        self.cells        = [[Cell(r, c) for c in range(self.cols)]
                              for r in range(self.rows)]
        self._initialized = False

    # --- Place les mines aléatoirement après le 1er clic du joueur ---
    def _place_mines(self, safe_row: int, safe_col: int):

        # On liste toutes les cases qui peuvent recevoir une mine
        # On exclut la zone 3x3 autour du 1er clic pour que le joueur ne perde jamais au départ
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if not (abs(r - safe_row) <= 1 and abs(c - safe_col) <= 1)
        ]

        # On pioche au hasard le bon nombre de cases parmi les candidates
        for r, c in random.sample(candidates, self.mines):
            self.cells[r][c].is_mine = True

        self._compute_neighbors()   # on calcule les chiffres maintenant que les mines sont placées
        self._initialized = True    # on indique que la grille est prête

    # --- Calcule le chiffre à afficher sur chaque case (nombre de mines autour) ---
    def _compute_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                # Inutile de compter pour une case qui est elle-même une mine
                if not self.cells[r][c].is_mine:
                    # On compte combien de voisins sont des mines et on stocke le résultat
                    self.cells[r][c].neighbor_count = sum(
                        1 for nr, nc in self._neighbors(r, c)
                        if self.cells[nr][nc].is_mine
                    )

    # --- Retourne la liste des coordonnées des cases voisines (max 8 autour) ---
    def _neighbors(self, row: int, col: int):
        # dr et dc sont des décalages de -1, 0 ou +1 en ligne et en colonne
        # Cela couvre les 8 directions : haut, bas, gauche, droite et les 4 diagonales
        return [
            (row + dr, col + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)               # on exclut la case elle-même (décalage nul)
            and 0 <= row + dr < self.rows        # on reste dans les limites verticales
            and 0 <= col + dc < self.cols        # on reste dans les limites horizontales
        ]

    # --- Révèle une case et se propage récursivement si elle est vide ---
    def reveal(self, row: int, col: int):
        cell = self.cells[row][col]

        # Cas de base : si la case est déjà révélée ou flagguée, on s'arrête
        if cell.revealed or cell.flagged:
            return

        cell.reveal()   # on découvre la case

        # Si la case est vide (aucune mine autour), on révèle aussi tous ses voisins
        # Chaque voisin fera de même → effet de propagation en cascade (flood-fill)
        if not cell.is_mine and cell.neighbor_count == 0:
            for nr, nc in self._neighbors(row, col):
                self.reveal(nr, nc)     # appel récursif sur chaque voisin

    # --- Pose ou retire un drapeau sur la case, en déléguant à l'objet Cell ---
    def toggle_flag(self, row: int, col: int):
        self.cells[row][col].toggle_flag()

    # --- Compte le nombre de drapeaux posés sur la grille ---
    # @property permet d'appeler grid.flags_placed sans parenthèses, comme un attribut
    @property
    def flags_placed(self):
        return sum(1 for row in self.cells for cell in row if cell.flagged)

    # --- Retourne True si toutes les cases sans mine sont révélées (condition de victoire) ---
    def is_victory(self):
        return all(
            cell.revealed
            for row in self.cells
            for cell in row
            if not cell.is_mine     # on ignore les mines, elles n'ont pas besoin d'être révélées
        )

    # --- Révèle toutes les mines d'un coup (appelé quand le joueur perd) ---
    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.revealed = True

    # --- Remet la grille à zéro en reconstruisant une grille vide ---
    def reset(self):
        self._build()

    # --- Demande à chaque case de se dessiner sur l'écran ---
    def draw(self, surface, font_num, font_icon):
        for row in self.cells:
            for cell in row:
                cell.draw(surface, font_num, font_icon)  # chaque case gère son propre rendu
