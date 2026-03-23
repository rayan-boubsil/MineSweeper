import pygame
from Button import Button
from Settings import *

class ScoreboardScreen:
    """Affiche les meilleurs scores enregistrés."""
    
    def __init__(self, manager):
        self.manager = manager
        # Un seul bouton pour revenir au menu principal
        self.btn_back = Button(300, 500, 200, 50, "BACK", lambda: self.manager.set_state("MAIN"))
        # Police d'écriture pour la liste des scores
        self.font_data = pygame.font.SysFont("Courier", 28)

    def handle_events(self, event):
        """Gère le clic sur le bouton retour."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.btn_back.handle_click()

    def update(self, mouse_pos):
        """Met à jour l'effet de survol du bouton retour."""
        self.btn_back.update(mouse_pos)

    def draw(self, surface):
        """Affiche le titre et la liste des scores."""
        # 1. On dessine le titre via le manager
        self.manager.draw_header(surface, "BEST TIMES")
        # 2. On récupère les scores depuis le ScoreManager
        scores_to_display = self.manager.score_manager.scores
        # 3. Boucle pour afficher chaque ligne de score
        for i, entry in enumerate(scores_to_display):
            name = entry.get("name", "---")
            time = entry.get("time", "--:--")
            # Formatage : Rang | Nom (sur 10 caractères) | Temps
            display_text = f"#{i+1}  {name:<10}  {time}"
            surf = self.font_data.render(display_text, True, COLOR_TEXT)
            # On décale chaque ligne vers le bas (180 + i * 45 pixels)
            surface.blit(surf, (SCREEN_WIDTH//2 - 150, 180 + i * 45))
        # 4. On dessine le bouton retour
        self.btn_back.draw(surface)