import random
from core.cell import Cell

class Grid:
    """
    Gère la logique pure de la grille du Démineur.
    Fichier de type 'Modèle' (Logique uniquement).
    """
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cells = []
        self._initialized = False 
        self._build()

    def _build(self):
        """Crée la matrice de cellules initiales."""
        # On ne stocke que les positions logiques (ligne, colonne)
        self.cells = [[Cell(r, c) for c in range(self.cols)]
                      for r in range(self.rows)]
        self._initialized = False

    def _place_mines(self, safe_row: int, safe_col: int):
        """Place les mines après le premier clic pour éviter de perdre immédiatement."""
        candidates = [
            (r, c) for r in range(self.rows)
            for c in range(self.cols)
            if not (r == safe_row and c == safe_col)
        ]
        
        # Sélection aléatoire sans doublons
        for r, c in random.sample(candidates, self.mines):
            self.cells[r][c].is_mine = True
        
        self._compute_neighbors()
        self._initialized = True

    def _compute_neighbors(self):
        """Calcule le nombre de mines adjacentes pour chaque case."""
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.cells[r][c].is_mine:
                    self.cells[r][c].neighbor_count = sum(
                        1 for nr, nc in self._neighbors(r, c)
                        if self.cells[nr][nc].is_mine
                    )

    def _neighbors(self, row: int, col: int):
        """Retourne les voisins valides (8 directions) sans déborder de la grille."""
        return [
            (row + dr, col + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)
            and 0 <= row + dr < self.rows
            and 0 <= col + dc < self.cols
        ]

    def reveal(self, row: int, col: int):
        """Logique de révélation avec propagation récursive."""
        if not self._initialized:
            self._place_mines(row, col)

        cell = self.cells[row][col]
        
        # On ignore si déjà révélé ou si marqué (drapeau/?)
        if cell.revealed or cell.marker_state != 0:
            return
            
        cell.reveal()

        # Si vide, on ouvre les voisins automatiquement
        if not cell.is_mine and cell.neighbor_count == 0:
            for nr, nc in self._neighbors(row, col):
                self.reveal(nr, nc)

    def toggle_flag(self, row: int, col: int):
        """Change l'état du marqueur via la cellule."""
        self.cells[row][col].toggle_flag()

    def get_flags_count(self):
        """Compte manuellement les drapeaux (état 1) sur toute la grille."""
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.marker_state == 1:
                    count += 1
        return count

    def is_victory(self):
        """Vérifie si le joueur a gagné (toutes les cases sans mine sont révélées)."""
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.revealed:
                    return False
        return True

    def reveal_all_mines(self):
        """Découvre toutes les mines lors d'un Game Over."""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.revealed = True

    def reset(self):
        """Réinitialise la grille."""
        self._build()