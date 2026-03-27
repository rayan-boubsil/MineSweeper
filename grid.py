import pygame
import random
from cell import Cell, CELL_SIZE, HEADER_H


class Grid:

    # --- Constructor called automatically when the grid is created ---
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows         = rows    # number of rows
        self.cols         = cols    # number of columns
        self.mines        = mines   # number of mines to place
        self.cells        = []      # will hold all cells (list of lists)
        self._initialized = False   # becomes True once mines are placed (after first click)
        self._build()               # build the empty grid right away

    # --- Creates an empty grid: a list of rows, each row containing cells ---
    def _build(self):
        # For each row r and column c, create a Cell object
        # Result: self.cells[r][c] gives the cell at row r, column c
        self.cells        = [[Cell(r, c) for c in range(self.cols)]
                              for r in range(self.rows)]
        self._initialized = False

    # --- Places mines randomly after the player's first click ---
    def _place_mines(self, safe_row: int, safe_col: int):

        # List all cells that can receive a mine
        # Exclude the 3x3 zone around the first click so the player never loses immediately
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if not (abs(r - safe_row) <= 1 and abs(c - safe_col) <= 1)
        ]

        # Randomly pick the right number of cells from the candidates
        for r, c in random.sample(candidates, self.mines):
            self.cells[r][c].is_mine = True

        self._compute_neighbors()   # calculate numbers now that mines are placed
        self._initialized = True    # mark the grid as ready

    # --- Calculates the number to display on each cell (mines around it) ---
    def _compute_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                # No need to count for a cell that is itself a mine
                if not self.cells[r][c].is_mine:
                    # Count how many neighbors are mines and store the result
                    self.cells[r][c].neighbor_count = sum(
                        1 for nr, nc in self._neighbors(r, c)
                        if self.cells[nr][nc].is_mine
                    )

    # --- Returns the list of coordinates of neighboring cells (up to 8) ---
    def _neighbors(self, row: int, col: int):
        # dr and dc are offsets of -1, 0 or +1 in row and column
        # This covers all 8 directions: up, down, left, right and the 4 diagonals
        return [
            (row + dr, col + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)               # exclude the cell itself (zero offset)
            and 0 <= row + dr < self.rows        # stay within vertical bounds
            and 0 <= col + dc < self.cols        # stay within horizontal bounds
        ]

    # --- Reveals a cell and recursively spreads if it is empty ---
    def reveal(self, row: int, col: int):
        cell = self.cells[row][col]

        # Base case: if the cell is already revealed, flagged or questioned, stop here
        if cell.revealed or cell.flagged or cell.questioned:
            return

        cell.reveal()   # uncover the cell

        # If the cell is empty (no mines around), reveal all its neighbors too
        # Each neighbor does the same -> cascade propagation effect (flood-fill)
        if not cell.is_mine and cell.neighbor_count == 0:
            for nr, nc in self._neighbors(row, col):
                self.reveal(nr, nc)     # recursive call on each neighbor

    # --- Cycles the cell state (normal -> flag -> ? -> normal), delegating to Cell ---
    def toggle_flag(self, row: int, col: int):
        self.cells[row][col].toggle_flag()

    # --- Returns the number of flags currently placed on the grid ---
    # @property allows calling grid.flags_placed without parentheses, like an attribute
    @property
    def flags_placed(self):
        return sum(1 for row in self.cells for cell in row if cell.flagged)

    # --- Returns True if all non-mine cells are revealed (victory condition) ---
    def is_victory(self):
        return all(
            cell.revealed
            for row in self.cells
            for cell in row
            if not cell.is_mine     # mines don't need to be revealed
        )

    # --- Reveals all mines at once (called when the player loses) ---
    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.revealed = True

    # --- Resets the grid by rebuilding a fresh empty grid ---
    def reset(self):
        self._build()

    # --- Asks every cell to draw itself on screen ---
    def draw(self, surface, font_num, font_icon):
        for row in self.cells:
            for cell in row:
                cell.draw(surface, font_num, font_icon)  # each cell handles its own rendering
