import pygame

class BaseScreen:
    def __init__(self, manager):
        self.manager = manager
        self.buttons = []

    def handle_events(self, event):
        # On gère les boutons une fois pour toutes
        for b in self.buttons:
            b.handle_event(event)

    def draw_common(self, surface, title_text):
        # 1. On nettoie (obligatoire pour le filtre clair)
        surface.fill((20, 25, 35))
        
        # 2. On appelle le header via le manager
        # VERIFIE BIEN QUE self.manager possède la méthode draw_header
        self.manager.draw_header(surface, title_text)

    def draw_buttons(self, surface):
        """Dessine les boutons à la fin pour qu'ils soient au-dessus."""
        for b in self.buttons:
            b.draw(surface)