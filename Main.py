import pygame
import sys
from Button import Button
from ScoreManager import ScoreManager
from Scoreboard import ScoreboardScreen
from AudioManager import AudioManager 
from Settings import *

class MenuManager:
    """Main controller for UI states."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper 3D")
        self.clock = pygame.time.Clock()
        self.state = "MAIN" 
        # --- Systems ---
        self.score_manager = ScoreManager() 
        # ==========================================
        # AUDIO : INITIALISATION
        # ==========================================
        self.audio = AudioManager() 
        # COMMENTAIRE : Lance la musique du menu ici.
        # Exemple : self.audio.start_music("assets/musique_menu.mp3")
        # ==========================================
        # --- Screens ---
        self.score_screen = ScoreboardScreen(self)
        # --- Main Menu buttons ---
        self.main_buttons = [
            Button(300, 220, 200, 60, "PLAY", lambda: self.set_state("GAME")), 
            Button(300, 300, 200, 60, "SCORES", lambda: self.set_state("SCORES")),
            Button(300, 380, 200, 60, "EXIT", sys.exit)
        ]

    def set_state(self, new_state):
        self.state = new_state
        # ==========================================
        # AUDIO : CHANGEMENT D'ÉTAT
        # ==========================================
        # Tu peux vérifier l'état ici pour changer de musique.
        # if new_state == "GAME":
        #     self.audio.start_music("assets/musique_jeu.mp3")
        # ==========================================

    def draw_background(self):
        self.screen.fill(COLOR_BG)

    def draw_header(self, surface, text):
        font = pygame.font.SysFont("Impact", 60)
        surf = font.render(text, True, COLOR_ACCENT)
        surface.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, 50))

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ==========================================
                    # AUDIO : BRUITAGE CLIC
                    # ==========================================
                    # Se déclenche à chaque clic de souris dans le menu.
                    self.audio.play_sfx("click") 
                    # ==========================================
                    if self.state == "MAIN":
                        for b in self.main_buttons: b.handle_click()
                    elif self.state == "SCORES":
                        self.score_screen.btn_back.handle_click()
            self.draw_background()
            if self.state == "MAIN":
                self.draw_header(self.screen, "MINESWEEPER 3D")
                for b in self.main_buttons:
                    b.update(mouse_pos)
                    b.draw(self.screen)
            elif self.state == "SCORES":
                self.score_screen.btn_back.update(mouse_pos)
                self.score_screen.draw(self.screen)
            elif self.state == "GAME":
                self.draw_header(self.screen, "GAME STARTING...")

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = MenuManager()
    app.run()