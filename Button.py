import pygame
from Settings import *

class Button:
    """Un bouton réutilisable qui change de couleur au survol."""
    
    def __init__(self, x, y, w, h, text, callback):
        # Position et taille du bouton
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback # La fonction à exécuter lors du clic
        
        # Style du texte
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        self.hovered = False

    def update(self, mouse_pos):
        """Vérifie si la souris survole le bouton."""
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        """Dessine le bouton avec un changement de couleur si survolé."""
        # 1. Choisir la couleur de fond (utilise les variables de Settings.py)
        color = COLOR_BTN_HOVER if self.hovered else COLOR_BTN
        # 2. Dessiner le rectangle principal (arrondi pour un look moderne)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        # 3. Dessiner la bordure (plus brillante si survolée)
        border_col = COLOR_ACCENT if self.hovered else (80, 80, 80)
        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=12)
        # 4. Préparer et centrer le texte
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        # 5. Afficher le texte sur le bouton
        surface.blit(text_surf, text_rect)

    def handle_click(self):
        """Exécute l'action associée au bouton si on clique dessus."""
        if self.hovered:
            self.callback()