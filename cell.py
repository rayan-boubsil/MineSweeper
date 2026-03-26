import pygame

CELL_SIZE   = 40
MARGIN      = 2
HEADER_H    = 80

C_HIDDEN    = (70,  80, 100)
C_REVEALED  = (200, 205, 215)
C_MINE_BG   = (220,  60,  60)
C_FLAG      = (240, 180,  30)
C_QUESTION  = (130, 180, 255)  # couleur du point d'interrogation (bleu clair)
C_BORDER_LT = (110, 125, 150)
C_BORDER_DK = (20,   25,  35)

NUMBER_COLORS = {
    1: (80,  130, 255),
    2: (50,  200, 100),
    3: (240,  80,  80),
    4: (130,  70, 200),
    5: (220, 100,  40),
    6: (60,  210, 210),
    7: (230,  50, 130),
    8: (160, 160, 160),
}


class Cell:
    def __init__(self, row: int, col: int):
        self.row            = row
        self.col            = col
        self.is_mine        = False
        self.revealed       = False
        self.flagged        = False
        self.questioned     = False  # True si la case porte un point d'interrogation
        self.neighbor_count = 0

    def reveal(self):
        # On ne peut révéler que si la case n'a ni drapeau ni point d'interrogation
        if not self.flagged and not self.questioned:
            self.revealed = True

    def toggle_flag(self):
        """
        Cycle des états au clic droit sur une case non révélée :
        normal → drapeau → point d'interrogation → normal → ...
        """
        if self.revealed:
            return
        if not self.flagged and not self.questioned:
            # état normal → on pose un drapeau
            self.flagged    = True
            self.questioned = False
        elif self.flagged and not self.questioned:
            # drapeau → on met un point d'interrogation
            self.flagged    = False
            self.questioned = True
        else:
            # point d'interrogation → on revient à l'état normal
            self.flagged    = False
            self.questioned = False

    def draw(self, surface, font_num, font_icon):
        x    = self.col * CELL_SIZE
        y    = self.row * CELL_SIZE + HEADER_H
        rect = pygame.Rect(
            x + MARGIN,
            y + MARGIN,
            CELL_SIZE - 2 * MARGIN,
            CELL_SIZE - 2 * MARGIN
        )

        if self.revealed:
            if self.is_mine:
                pygame.draw.rect(surface, C_MINE_BG, rect, border_radius=4)
                txt = font_icon.render("*", True, (255, 255, 255))
                surface.blit(txt, txt.get_rect(center=rect.center))
            else:
                pygame.draw.rect(surface, C_REVEALED, rect, border_radius=4)
                if self.neighbor_count > 0:
                    color = NUMBER_COLORS.get(self.neighbor_count, (0, 0, 0))
                    txt = font_num.render(str(self.neighbor_count), True, color)
                    surface.blit(txt, txt.get_rect(center=rect.center))
        else:
            # Fond de la case cachée avec effet 3D
            pygame.draw.rect(surface, C_HIDDEN, rect, border_radius=4)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.topright, 2)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.topright, rect.bottomright, 2)

            if self.flagged:
                # Drapeau : F en jaune
                txt = font_icon.render("🚩", True, C_FLAG)
                surface.blit(txt, txt.get_rect(center=rect.center))
            elif self.questioned:
                # Point d'interrogation : ? en bleu clair
                txt = font_icon.render("?", True, C_QUESTION)
                surface.blit(txt, txt.get_rect(center=rect.center))
