import pygame
import sys
from ScoreManager import ScoreManager
from Scoreboard import ScoreboardScreen
from AudioManager import AudioManager 
from DifficultyMenu import DifficultyMenu
from MainMenu import MainMenu
from Settings import *

class MainLoop:
    """Le contrôleur principal qui fait tourner le jeu et gère les écrans."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper 3D")
        self.clock = pygame.time.Clock()
        # --- États et Données ---
        self.state = "MAIN" 
        self.current_config = None # Contiendra la difficulté choisie (EASY, etc.)
        # --- Systèmes (Outils) ---
        self.score_manager = ScoreManager() 
        self.audio = AudioManager() 
        # --- Écrans (Interfaces) ---
        self.main_menu = MainMenu(self)
        self.score_screen = ScoreboardScreen(self)
        self.difficulty_screen = DifficultyMenu(self)

    # --- Fonctions Utilitaires ---
    def set_state(self, new_state):
        """Change l'écran actif."""
        self.state = new_state

    def quit_game(self):
        """Ferme proprement le programme."""
        pygame.quit()
        sys.exit()

    def draw_header(self, surface, text):
        """Affiche un titre stylisé en haut de l'écran."""
        font = pygame.font.SysFont("Impact", 60)
        surf = font.render(text, True, COLOR_ACCENT)
        surface.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, 50))

    # --- Cœur du programme (Logic & Rendering) ---
    def update(self, mouse_pos):
        """Met à jour la logique des boutons (survol)."""
        if self.state == "MAIN":
            self.main_menu.update(mouse_pos)
        elif self.state == "DIFFICULTY":
            self.difficulty_screen.update(mouse_pos)
        elif self.state == "SCORES":
            self.score_screen.btn_back.update(mouse_pos)

    def draw(self):
        """Dessine l'interface selon l'état actuel."""
        self.screen.fill(COLOR_BG) # Fond de base
        if self.state == "MAIN":
            self.main_menu.draw(self.screen)
        elif self.state == "DIFFICULTY":
            self.difficulty_screen.draw(self.screen)
        elif self.state == "SCORES":
            self.score_screen.draw(self.screen)
        elif self.state == "GAME":
            self.draw_header(self.screen, "IN GAME...")
        pygame.display.flip() # Rafraîchissement visuel

    def run(self):
        """Boucle infinie du jeu."""
        while True:
            mouse_pos = pygame.mouse.get_pos()
            # 1. Gestion des événements (Clavier / Souris)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.audio.play_sfx("click") 
                # Délégation des clics aux écrans
                if self.state == "MAIN":
                    self.main_menu.handle_events(event)
                elif self.state == "DIFFICULTY":
                    self.difficulty_screen.handle_events(event)
                elif self.state == "SCORES":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.score_screen.btn_back.handle_click()
            # 2. Mise à jour de la logique
            self.update(mouse_pos)
            # 3. Dessin
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = MainLoop()
    app.run()