import pygame
from Settings import *
from InputBox import InputBox
class GameOverScreen:
    """Screen displayed after a win/loss to save the score."""
    def __init__(self, manager):
        self.manager = manager
        self.input_box = InputBox(300, 300, 200, 50)
        self.final_time = "00:00"
        self.current_mode = "CLASSIC"

    def set_results(self, time_str, mode):
        self.final_time = time_str
        self.current_mode = mode

    def update(self, events):
        for event in events:
            name = self.input_box.handle_event(event)
            if name: # If ENTER was pressed and name is returned
                # Save to JSON via our ScoreManager
                self.manager.score_manager.add_score(self.current_mode, name, self.final_time)
                # Go back to main menu
                self.manager.set_state("MAIN")

    def draw(self, screen):
        screen.fill((20, 20, 25))
        # Display Results
        font = pygame.font.SysFont("Impact", 50)
        msg = font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 100))
        
        res_font = pygame.font.SysFont("Arial", 30)
        res_text = res_font.render(f"TIME: {self.final_time} | MODE: {self.current_mode}", True, (255, 255, 255))
        screen.blit(res_text, (SCREEN_WIDTH//2 - res_text.get_width()//2, 200))
        
        self.input_box.draw(screen)