import pygame

CELL_SIZE   = 40
MARGIN      = 2
HEADER_H    = 80

C_HIDDEN    = (70,  80, 100)
C_REVEALED  = (200, 205, 215)
C_MINE_BG   = (220,  60,  60)
C_FLAG      = (240, 180,  30)
C_BORDER_LT = (110, 125, 150)
C_BORDER_DK = (20,  25,  35)

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
        self.neighbor_count = 0

    def reveal(self):
        if not self.flagged:
            self.revealed = True

    def toggle_flag(self):
        if not self.revealed:
            self.flagged = not self.flagged

    def draw(self, surface, font_num, font_icon):
        x    = self.col * CELL_SIZE
        y    = self.row * CELL_SIZE + HEADER_H
        rect = pygame.Rect(x + MARGIN, y + MARGIN,
                           CELL_SIZE - 2*MARGIN, CELL_SIZE - 2*MARGIN)

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
            pygame.draw.rect(surface, C_HIDDEN, rect, border_radius=4)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.topright, 2)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.topright, rect.bottomright, 2)
            if self.flagged:
                txt = font_icon.render("🚩", True, C_FLAG)
                surface.blit(txt, txt.get_rect(center=rect.center))
