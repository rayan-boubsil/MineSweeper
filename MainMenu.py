import pygame
from Button import Button
from Settings import *

class MainMenu:
    """L'écran d'accueil du jeu."""
    
    def __init__(self, manager):
        self.manager = manager
        # Création des boutons principaux du menu
        self.buttons = [
            # Direction l'écran de difficulté
            Button(100, 220, 250, 60, "PLAY", lambda: self.manager.set_state("DIFFICULTY")), 
            # Direction l'écran des scores
            Button(100, 300, 250, 60, "SCORES", lambda: self.manager.set_state("SCORES")),
            # Quitte le jeu
            Button(100, 380, 250, 60, "EXIT", self.manager.quit_game)
        ]

    def handle_events(self, event):
        """Gère les clics sur les boutons du menu principal."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in self.buttons:
                b.handle_click()

    def update(self, mouse_pos):
        """Met à jour l'état de survol des boutons."""
        for b in self.buttons:
            b.update(mouse_pos)

    def draw(self, surface):
        """Affiche le titre et les boutons sur l'écran."""
        # On demande au manager de dessiner le gros titre "MINESWEEPER 3D"
        self.manager.draw_header(surface, "MINESWEEPER 3D")
        pygame.draw.line(surface, COLOR_ACCENT, (70, 180), (70, 480), 2)
        # On dessine chaque bouton
        for b in self.buttons:
            b.draw(surface)