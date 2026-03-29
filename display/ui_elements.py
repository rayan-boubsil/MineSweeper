import pygame
from constants import * 
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback 
        self.visible = True 
        self.active = True  # <-- AJOUT : Par défaut, le bouton est cliquable
        
        try:
            self.font = pygame.font.Font(None, 28) 
        except:
            self.font = pygame.font.SysFont("Verdana", 22, bold=True)
        self.hovered = False

    def check_hover(self, mouse_pos):
        # On ne permet le hover que si le bouton est actif
        if self.active:
            self.hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.hovered = False

    def draw(self, surface):
        if not self.visible: return        
        # --- LOGIQUE DE COULEUR ---
        if not self.active:
            # Style bouton verrouillé (LOCKED)
            color_bg = C_BLACK
            color_border = C_LOCKED_GREY
            text_col = (80, 80, 80)
            draw_rect = self.rect
        else:
            # Style Matrix Actif
            # On garde ton idée d'offset (décalage) si tu aimes l'animation
            offset = 8 if self.hovered else 0
            draw_rect = self.rect.copy()
            draw_rect.x += offset 
            
            # Le fond devient vert sombre au survol, sinon noir
            color_bg = C_GREEN_DARK if self.hovered else C_BLACK
            color_border = C_GREEN_NEON
            text_col = C_GREEN_NEON

        # 1. Dessin du fond du bouton
        pygame.draw.rect(surface, color_bg, draw_rect, border_radius=5)
        
        # 2. Dessin de la bordure "Neon"
        # Plus épaisse (3px) si survolé, sinon fine (1px)
        border_width = 3 if self.hovered and self.active else 1
        pygame.draw.rect(surface, color_border, draw_rect, border_width, border_radius=5)
        
        # 3. Barre d'accentuation Matrix (à gauche)
        if self.active and self.hovered:
            # Une barre de 4px de large, vert fluo pur
            pygame.draw.rect(surface, (140, 255, 140), (draw_rect.x, draw_rect.y, 4, draw_rect.height), border_radius=5)

        # 4. Dessin du texte
        display_text = "LOCKED" if not self.active and self.text == "NOUVELLE PARTIE" else self.text
        text_surf = self.font.render(display_text, True, text_col)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        # On ajoute "not self.active" dans la condition de refus
        if not self.visible or not self.active or self.callback is None:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.callback()
                return True 
        return False