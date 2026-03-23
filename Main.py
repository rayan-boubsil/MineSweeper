import pygame
import sys
from Button import Button
from Particle import Particle
from ScoreManager import ScoreManager
from Scoreboard import ScoreboardScreen
from SelectionMode import ModeSelectionScreen
from Settings import *

class MenuManager:
    """Main controller for UI states."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper 3d")
        self.clock = pygame.time.Clock()
        self.state = "MAIN" 
        # --- Systems ---
        self.score_manager = ScoreManager() # Manages JSON saving/loading
        self.particles = [Particle(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(60)]   # On donne SCREEN_WIDTH et SCREEN_HEIGHT à chaque particule au moment de sa création
        # --- Screens ---
        self.score_screen = ScoreboardScreen(self)
        self.mode_screen = ModeSelectionScreen(self)
        # --- Main Menu buttons ---
        self.main_buttons = [
            Button(300, 220, 200, 60, "PLAY", lambda: self.set_state("MODES")),
            Button(300, 300, 200, 60, "SCORES", lambda: self.set_state("SCORES")),
            Button(300, 380, 200, 60, "EXIT", sys.exit)
        ]
    def set_state(self, new_state):
        self.state = new_state

    def draw_background(self):
        """Standardized background for all menu screens."""
        self.screen.fill(COLOR_BG)
        for p in self.particles:
            p.update()
            p.draw(self.screen)

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
                    if self.state == "MAIN":
                        for b in self.main_buttons: b.handle_click()
                    elif self.state == "SCORES":
                        self.score_screen.btn_back.handle_click()
                    elif self.state == "MODES":
                        for b in self.mode_screen.buttons: b.handle_click()
            # --- Logic / Update ---
            self.draw_background() # Always update/draw background particles
            if self.state == "MAIN":
                self.draw_header(self.screen, "MINESWEEPER 3d")
                for b in self.main_buttons:
                    b.update(mouse_pos)
                    b.draw(self.screen)
            elif self.state == "SCORES":
                self.score_screen.btn_back.update(mouse_pos)
                self.score_screen.draw(self.screen) # Now draws over particles
            elif self.state == "MODES":
                for b in self.mode_screen.buttons:
                    b.update(mouse_pos)
                self.mode_screen.draw(self.screen) # Now draws over particles
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = MenuManager()
    app.run()