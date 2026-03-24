import pygame
from Settings import *

class Button:
    """Un bouton réutilisable qui change de couleur au survol."""
    
    def __init__(self, x, y, w, h, text, callback):
        # Position et taille du bouton
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback 
        # --- CHARGEMENT DE LA POLICE ---
        try:
            # ATTENTION : On retire 'bold=True' ici, car .Font() ne le gère pas
            self.font = pygame.font.Font(FONT_CUSTOM, 28) 
        except:
            # Ici SysFont accepte bold=True
            self.font = pygame.font.SysFont("Verdana", 22, bold=True)
            print(f"Erreur : Impossible de charger {FONT_CUSTOM}")
        self.hovered = False

    def update(self, mouse_pos):
        """Vérifie si la souris survole le bouton."""
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # Si survolé, on décale un peu le bouton vers la droite (effet de mouvement)
        offset = 10 if self.hovered else 0
        draw_rect = self.rect.copy()
        draw_rect.x += offset 
        color = COLOR_BTN_HOVER if self.hovered else COLOR_BTN
        pygame.draw.rect(surface, color, draw_rect, border_radius=12)
        # Ajout d'une petite barre lumineuse sur le côté gauche si survolé
        if self.hovered:
            pygame.draw.rect(surface, COLOR_ACCENT, (draw_rect.x, draw_rect.y, 5, draw_rect.height), border_radius=12)
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_click(self):
        """Exécute l'action associée au bouton si on clique dessus."""
        if self.hovered:
            self.callback()