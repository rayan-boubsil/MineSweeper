import pygame
from Settings import *

class Button:
    """Reusable UI Button with hover effect and callback."""
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        color = COLOR_BTN_HOVER if self.hovered else COLOR_BTN
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        # Accent border
        border_col = COLOR_ACCENT if self.hovered else (80, 80, 80)
        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=12)
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_click(self):
        if self.hovered:
            self.callback()