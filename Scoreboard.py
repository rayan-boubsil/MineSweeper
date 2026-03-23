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
        # 1. On laisse le MenuManager dessiner le fond animé (particules)
        self.manager.draw_background() 
        # 2. Title
        font_title = pygame.font.SysFont("Impact", 50)
        title_surf = font_title.render("HALL OF FAME", True, COLOR_ACCENT)
        surface.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        # 3. List display
        font_data = pygame.font.SysFont("Courier", 25)
        # IMPORTANT: Get scores from the manager's score_manager
        scores_to_display = self.manager.score_manager.scores
        for i, entry in enumerate(scores_to_display):
            # Access data using dictionary keys
            mode = entry["mode"]
            name = entry["name"]
            time = entry["time"]
            # Formatting the string for a clean table look
            display_text = f"{mode:<12} | {name:<10} | {time}"
            surf = font_data.render(display_text, True, COLOR_TEXT)
            surface.blit(surf, (150, 180 + i * 40))
        # 4. Draw the back button
        self.btn_back.draw(surface)