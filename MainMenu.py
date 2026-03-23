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
            Button(300, 220, 200, 60, "PLAY", lambda: self.manager.set_state("DIFFICULTY")), 
            # Direction l'écran des scores
            Button(300, 300, 200, 60, "SCORES", lambda: self.manager.set_state("SCORES")),
            # Quitte le jeu
            Button(300, 380, 200, 60, "EXIT", self.manager.quit_game)
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
        # On dessine chaque bouton
        for b in self.buttons:
            b.draw(surface)