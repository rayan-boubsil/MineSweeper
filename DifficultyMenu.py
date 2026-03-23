import pygame
from Button import Button
from Settings import *

class DifficultyMenu:
    """Écran de sélection de la difficulté."""
    
    def __init__(self, manager):
        self.manager = manager
        # Création des boutons (Positions X, Y, Largeur, Hauteur)
        self.buttons = [
            Button(300, 200, 200, 60, "EASY", lambda: self.start_with("EASY")),
            Button(300, 280, 200, 60, "MEDIUM", lambda: self.start_with("MEDIUM")),
            Button(300, 360, 200, 60, "HARD", lambda: self.start_with("HARD")),
            Button(300, 460, 200, 50, "BACK", lambda: self.manager.set_state("MAIN"))
        ]

    def start_with(self, level):
        """Récupère la configuration et l'affiche sans lancer le jeu."""
        # 1. On va chercher les infos dans Settings.py
        config = DIFFICULTIES[level]
        # 2. On affiche les infos dans la console pour vérification
        print(f"--- SÉLECTION DÉTECTÉE ---")
        print(f"Mode : {level} | Grille : {config['rows']}x{config['cols']} | Mines : {config['mines']}")
        # 3. On stocke le choix dans le 'manager' pour plus tard
        self.manager.current_config = config
        # 4. Le changement d'état est désactivé pour tes tests (commente avec #)
        # self.manager.set_state("GAME")

    def handle_events(self, event):
        """Détecte les clics sur les boutons."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in self.buttons:
                b.handle_click()

    def update(self, mouse_pos):
        """Met à jour l'effet de survol (hover) des boutons."""
        for b in self.buttons:
            b.update(mouse_pos)

    def draw(self, surface):
        """Dessine le titre et les boutons sur l'écran."""
        self.manager.draw_header(surface, "SELECT DIFFICULTY")
        for b in self.buttons:
            b.draw(surface)