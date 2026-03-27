import pygame
from constants import *
from display.ui_elements import Button

class GameUI:
    def __init__(self, game):
        self.game = game
        bx = (SCREEN_WIDTH - 200) // 2
        
        # Boutons de Pause
        self.pause_buttons = [
            Button(bx, 250, 200, 45, "REPRENDRE", callback=game.toggle_pause),
            Button(bx, 310, 200, 45, "MENU", callback=lambda: game.manager.set_state("MAIN")),
            Button(bx, 370, 200, 45, "QUITTER", callback=game.manager.quit_game)
        ]
        
        # Boutons de Fin
        self.end_buttons = [
            Button(bx, 350, 200, 45, "REJOUER", callback=lambda: game.manager.set_state("GAME", game.config)),
            Button(bx, 410, 200, 45, "MENU", callback=lambda: game.manager.set_state("MAIN"))
        ]

    def update(self, mouse_pos):
        """Met à jour l'état de survol des boutons actifs."""
        if self.game.game_over:
            for btn in self.end_buttons: btn.check_hover(mouse_pos)
        elif self.game.paused:
            for btn in self.pause_buttons: btn.check_hover(mouse_pos)

    def handle_events(self, event):
        """Distribue les clics aux boutons actifs."""
        if self.game.game_over:
            for btn in self.end_buttons: btn.handle_event(event)
        elif self.game.paused:
            for btn in self.pause_buttons: btn.handle_event(event)