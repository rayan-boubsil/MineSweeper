import pygame
import random
from cell import Cell, CELL_SIZE, HEADER_H


class Grid:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows         = rows
        self.cols         = cols
        self.mines        = mines
        self.cells        = []
        self._initialized = False
        self._build()

    def _build(self):
        self.cells        = [[Cell(r, c) for c in range(self.cols)]
                              for r in range(self.rows)]
        self._initialized = False

    def _place_mines(self, safe_row: int, safe_col: int):
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if not (abs(r - safe_row) <= 1 and abs(c - safe_col) <= 1)
        ]
        for r, c in random.sample(candidates, self.mines):
            self.cells[r][c].is_mine = True
        self._compute_neighbors()
        self._initialized = True

    def _compute_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.cells[r][c].is_mine:
                    self.cells[r][c].neighbor_count = sum(
                        1 for nr, nc in self._neighbors(r, c)
                        if self.cells[nr][nc].is_mine
                    )

    def _neighbors(self, row: int, col: int):
        return [
            (row + dr, col + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)
            and 0 <= row + dr < self.rows
            and 0 <= col + dc < self.cols
        ]

    def reveal(self, row: int, col: int):
        cell = self.cells[row][col]
        if cell.revealed or cell.flagged:
            return
        cell.reveal()
        if not cell.is_mine and cell.neighbor_count == 0:
            for nr, nc in self._neighbors(row, col):
                self.reveal(nr, nc)

    def toggle_flag(self, row: int, col: int):
        self.cells[row][col].toggle_flag()

    @property
    def flags_placed(self):
        return sum(1 for row in self.cells for cell in row if cell.flagged)

    def is_victory(self):
        return all(
            cell.revealed
            for row in self.cells
            for cell in row
            if not cell.is_mine
        )

    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.revealed = True

    def reset(self):
        self._build()

    def draw(self, surface, font_num, font_icon):
        for row in self.cells:
            for cell in row:
                cell.draw(surface, font_num, font_icon)
