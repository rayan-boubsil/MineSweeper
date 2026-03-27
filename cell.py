import pygame

# --- Size of one cell in pixels ---
CELL_SIZE   = 40

# --- Gap between cells so they don't touch each other ---
MARGIN      = 2

# --- Height of the top header bar in pixels ---
HEADER_H    = 80

# --- Colors in RGB format (Red, Green, Blue), each value between 0 and 255 ---
C_HIDDEN    = (70,  80, 100)   # unrevealed cell (blue-gray)
C_REVEALED  = (200, 205, 215)  # revealed cell (light gray)
C_MINE_BG   = (220,  60,  60)  # background of an exploded mine (red)
C_FLAG      = (240, 180,  30)  # flag color (yellow)
C_QUESTION  = (130, 180, 255)  # question mark color (light blue)
C_BORDER_LT = (110, 125, 150)  # light border (top and left sides) for the 3D effect
C_BORDER_DK = (20,   25,  35)  # dark border (bottom and right sides) for the 3D effect

# --- Color for each number (1 to 8) displayed on a revealed cell ---
NUMBER_COLORS = {
    1: (80,  130, 255),  # blue
    2: (50,  200, 100),  # green
    3: (240,  80,  80),  # red
    4: (130,  70, 200),  # purple
    5: (220, 100,  40),  # orange
    6: (60,  210, 210),  # cyan
    7: (230,  50, 130),  # pink
    8: (160, 160, 160),  # gray
}


class Cell:
    # --- Constructor called automatically when a new cell is created ---
    def __init__(self, row: int, col: int):
        self.row            = row       # row number in the grid
        self.col            = col       # column number in the grid
        self.is_mine        = False     # True if this cell contains a mine
        self.revealed       = False     # True if the player clicked on it
        self.flagged        = False     # True if the player placed a flag
        self.questioned     = False     # True if the cell has a question mark
        self.neighbor_count = 0         # number of mines in the 8 surrounding cells

    # --- Reveals the cell, unless it has a flag or a question mark ---
    def reveal(self):
        if not self.flagged and not self.questioned:
            self.revealed = True

    def toggle_flag(self):
        """
        Cycles through states on right-click on an unrevealed cell:
        normal -> flag -> question mark -> normal -> ...
        """
        if self.revealed:
            return
        if not self.flagged and not self.questioned:
            # normal state -> place a flag
            self.flagged    = True
            self.questioned = False
        elif self.flagged and not self.questioned:
            # flag -> switch to question mark
            self.flagged    = False
            self.questioned = True
        else:
            # question mark -> go back to normal state
            self.flagged    = False
            self.questioned = False

    # --- Draws the cell on screen based on its current state ---
    def draw(self, surface, font_num, font_icon):

        # Calculate the pixel position from the row and column numbers
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE + HEADER_H  # + HEADER_H to skip the top bar

        # Build the cell rectangle with margin applied to space cells apart
        rect = pygame.Rect(
            x + MARGIN,
            y + MARGIN,
            CELL_SIZE - 2 * MARGIN,
            CELL_SIZE - 2 * MARGIN
        )

        if self.revealed:
            if self.is_mine:
                # Revealed mine: red background with a star symbol
                pygame.draw.rect(surface, C_MINE_BG, rect, border_radius=4)
                txt = font_icon.render("*", True, (255, 255, 255))
                surface.blit(txt, txt.get_rect(center=rect.center))
            else:
                # Revealed safe cell: light gray background
                pygame.draw.rect(surface, C_REVEALED, rect, border_radius=4)

                # If there are mines nearby, display their count in color
                if self.neighbor_count > 0:
                    color = NUMBER_COLORS.get(self.neighbor_count, (0, 0, 0))
                    txt = font_num.render(str(self.neighbor_count), True, color)
                    surface.blit(txt, txt.get_rect(center=rect.center))

        else:
            # Unrevealed cell: blue-gray background with a 3D border effect
            pygame.draw.rect(surface, C_HIDDEN, rect, border_radius=4)

            # Light borders on top and left -> raised 3D effect
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.topright, 2)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.bottomleft, 2)

            # Dark borders on bottom and right -> reinforces the 3D effect
            pygame.draw.line(surface, C_BORDER_DK, rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.topright, rect.bottomright, 2)

            if self.flagged:
                # Flag: yellow F in the center
                txt = font_icon.render("F", True, C_FLAG)
                surface.blit(txt, txt.get_rect(center=rect.center))
            elif self.questioned:
                # Question mark: light blue ? in the center
                txt = font_icon.render("?", True, C_QUESTION)
                surface.blit(txt, txt.get_rect(center=rect.center))
