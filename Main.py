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
        self.state_names = {
            "MAIN": "MENU PRINCIPAL",
            "DIFFICULTY": "CHOIX DE DIFFICULTÉ",
            "SCORES": "MEILLEURS SCORES"
        }
    # --- Fonctions Utilitaires ---
    def set_state(self, new_state):
        """Change l'écran actif."""
        self.state = new_state

    def quit_game(self):
        """Ferme proprement le programme."""
        pygame.quit()
        sys.exit()

    def draw_header(self, surface, text):
        """Affiche le titre de l'écran avec les réglages centralisés."""
        try:
            # On utilise la taille définie dans Settings
            font = pygame.font.Font(FONT_CUSTOM, TITLE_FONT_SIZE)
        except:
            font = pygame.font.SysFont("Impact", TITLE_FONT_SIZE)
        surf = font.render(text, True, COLOR_ACCENT)
        # Calcul de la position avec les constantes
        pos_x = (SCREEN_WIDTH // 2) - (surf.get_width() // 2) + TITLE_X_OFFSET
        pos_y = TITLE_Y_POS
        surface.blit(surf, (pos_x, pos_y))

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
        self.screen.fill(COLOR_BG) # 1. Fond de base
        # --- 2. NOUVEAU : INDICATEUR DE POSITION (Haut à Droite) ---
        # On ne l'affiche que si on n'est PAS en train de jouer
        if self.state != "GAME":
            # On récupère le nom depuis le dictionnaire (ex: "MENU PRINCIPAL")
            current_name = self.state_names.get(self.state, "")
            if current_name:
                font_nav = pygame.font.SysFont("Verdana", 14, bold=True)
                nav_surf = font_nav.render(current_name, True, COLOR_ACCENT)
                # Position : à 30px du bord droit et 25px du haut
                nav_x = SCREEN_WIDTH - nav_surf.get_width() - 30
                nav_y = 25
                self.screen.blit(nav_surf, (nav_x, nav_y))
                # Trait horizontal décoratif
                line_y = nav_y + nav_surf.get_height() + 5
                pygame.draw.line(self.screen, COLOR_ACCENT, (nav_x, line_y), (SCREEN_WIDTH - 30, line_y), 2)
        # --- 3. DESSIN DES ÉCRANS ---
        if self.state == "MAIN":
            self.main_menu.draw(self.screen)
        elif self.state == "DIFFICULTY":
            self.difficulty_screen.draw(self.screen)
        elif self.state == "SCORES":
            self.score_screen.draw(self.screen)
        elif self.state == "GAME":
            self.draw_header(self.screen, "IN GAME...")
        pygame.display.flip() # 4. Rafraîchissement visuel

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