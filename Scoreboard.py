import pygame
from Button import Button
from Settings import *

class ScoreboardScreen:
    """Handles high score display logic."""
    def __init__(self, manager):
        self.manager = manager
        # Example scores: Mode, Name, Time
        self.scores = [
            ("CLASSIC", "ALEX", "00:54"),
            ("FRENZY", "SAM", "01:12"),
            ("DARK", "LUNA", "00:30")
        ]
        self.btn_back = Button(300, 500, 200, 50, "BACK", lambda: self.manager.set_state("MAIN"))

    def draw(self, surface):
        self.manager.draw_background()
        self.manager.draw_header(surface, "BEST TIMES")
        
        font_data = pygame.font.SysFont("Courier", 30)
        scores_to_display = self.manager.score_manager.scores
        
        for i, entry in enumerate(scores_to_display):
            name = entry["name"]
            time = entry["time"]
            
            # On affiche juste Rang | Nom | Temps
            display_text = f"#{i+1}  {name:<10}  {time}"
            
            surf = font_data.render(display_text, True, COLOR_TEXT)
            # On centre un peu plus l'affichage
            surface.blit(surf, (SCREEN_WIDTH//2 - 150, 180 + i * 45))
        
        self.btn_back.draw(surface)