import pygame
import time
import random
from core.grid import Grid
from constants import *
from display.renderer import GameRenderer
from display.game_ui import GameUI

class Game:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.grid = Grid(config["rows"], config["cols"], config["mines"])
        self.renderer = GameRenderer() # <--- On crée l'objet ici
        self.reset_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, 20, 50, 50)
        # États
        self.paused = False
        self.game_over = False
        self.won = False
        # Chrono
        self.start_time = None
        self.elapsed_before_pause = 0
        self.elapsed_time = 0
        # Initialisation de l'UI déportée
        self.ui = GameUI(self)

    def update(self):
        self.ui.update(pygame.mouse.get_pos())
        if self.start_time and not self.paused and not self.game_over:
            self.elapsed_time = self.elapsed_before_pause + int(time.time() - self.start_time)

    def handle_event(self, event):
        # 1. Gestion des touches système (toujours actives : Pause, Reset, Quitter)
        if event.type == pygame.KEYDOWN:
            # Toggle Pause (P ou Echap)
            if event.key in [pygame.K_ESCAPE, pygame.K_p] and not self.game_over:
                self.toggle_pause()
                return # On s'arrête là pour cet événement
            # Reset (R)
            if event.key == pygame.K_r:
                self.reset()
                return
            # Quitter ou Menu (Q)
            if event.key == pygame.K_q:
                # On sauvegarde si la partie est encore en cours (facultatif selon ton envie)
                if not self.game_over and not self.won:
                    self.save_current_state()
                # On change l'état pour revenir au menu
                self.manager.set_state("MAIN")
                return
        # 2. Priorité UI (Si Pause ou Fin, on check les clics sur les boutons de l'UI)
        if self.game_over or self.paused:
            self.ui.handle_events(event)
            return # IMPORTANT : On ne clique pas sur la grille si l'UI est active
        # 3. Gameplay (Smiley & Grille) - Uniquement si PAS de pause/game_over
        mx, my = pygame.mouse.get_pos()
        # Clic sur le Smiley Reset
        if event.type == pygame.MOUSEBUTTONDOWN and self.reset_btn_rect.collidepoint(mx, my):
            self.reset()
            return
        # Clics sur la Grille
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._process_grid_click(mx, my, event.button)

    def _process_grid_click(self, mx, my, button):
        c_size = CELL_SIZE
        grid_w = self.grid.cols * c_size
        # On calcule l'offset X dynamiquement pour que la grille reste centrée
        x_off = (SCREEN_WIDTH - grid_w) // 2
        # Conversion des coordonnées pixels (mx, my) en coordonnées logiques (col, row)
        col = (mx - x_off) // c_size
        row = (my - GRID_OFFSET_Y) // c_size
        # Vérification que le clic est bien à l'intérieur des limites de la grille
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            if button == 1: 
                # Clic gauche : on révèle
                self.handle_click(row, col)
            elif button == 3: 
                # Clic droit : on change le marqueur (Drapeau/?)
                self.grid.toggle_flag(row, col) # <--- Utilise la méthode de Grid

    def handle_click(self, row, col):
        if not self.grid._initialized:
            self.grid._place_mines(row, col)
            self.start_time = time.time()
        cell = self.grid.cells[row][col]
        if cell.marker_state == 0 and not cell.revealed:
            self.grid.reveal(row, col)
            if cell.is_mine: self.end_game(False)
            elif self.grid.is_victory(): self.end_game(True)

    def end_game(self, won):
        self.won, self.game_over = won, True
        self.manager.audio.play_sfx("win" if won else "explosion")
        if not won: self.grid.reveal_all_mines()
        status = "(WIN)" if won else "(LOST)"
        self.manager.score_manager.add_score(
            self.config.get("difficulty", "EASY"), # On récupère la difficulté
            f"{self.manager.current_player_name} {status}", 
            self.elapsed_time
        )
        # Nettoyage de la sauvegarde
        self.manager.save_manager.delete_save(self.manager.current_player_name)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            if self.start_time: self.elapsed_before_pause += int(time.time() - self.start_time)
            self.save_current_state()
        else:
            self.start_time = time.time()

    def reset(self):
        self.__init__(self.manager, self.config)

    def save_current_state(self):
        data = {
            "config": self.config, "grid": self.grid,
            "elapsed_before_pause": self.elapsed_time,
            "won": self.won, "game_over": self.game_over
        }
        self.manager.save_manager.save_game(data, self.manager.current_player_name)
        
    def apply_save_data(self, data):
        self.grid = data["grid"]
        self.elapsed_before_pause = data["elapsed_before_pause"]
        self.elapsed_time = data["elapsed_before_pause"]
        self.won, self.game_over = data["won"], data["game_over"]
        if not self.game_over and not self.won: self.start_time = time.time()

    def draw(self, surface):
        # 1. On remplit le fond
        surface.fill(COLOR_BG) 
        # 2. On appelle le HUD via le Renderer (L'Option B)
        # On lui passe les polices stockées dans le manager
        self.renderer.draw_hud(surface, self, self.manager.font_ui, self.manager.font_icon)
        # 3. On dessine la grille
        # On utilise la méthode draw_grid de ton Renderer
        self.renderer.draw_grid(surface, self.grid, self.manager.font_num, self.manager.font_icon,CELL_SIZE)
        # 4. Gestion des Overlays (Pause / Fin)
        if self.paused:
            self.renderer.draw_pause_overlay(surface, self.manager.font_ui)
        elif self.game_over or self.won:
            self.renderer.draw_end_overlay(surface, self.won)

    def _draw_overlay(self, surface, title, title_color):
        """Dessine un calque semi-transparent avec les instructions."""
        # 1. Fond sombre
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        surface.blit(overlay, (0, 0))
        # 2. Polices
        font_big = pygame.font.SysFont("Verdana", 45, bold=True)
        font_small = pygame.font.SysFont("Verdana", 18, bold=True)
        # 3. Titre (GAME OVER ou PAUSE)
        title_surf = font_big.render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        surface.blit(title_surf, title_rect)
        # 4. Instructions (Raccourcis clavier)
        # On définit les lignes de texte selon l'état
        if self.game_over:
            lines = [
                ("R : RECOMMENCER", (200, 200, 200)),
                ("Q : QUITTER VERS LE MENU", (255, 100, 100))
            ]
        else: # Cas de la Pause
            lines = [
                ("P / ECHAP : REPRENDRE", (100, 255, 100)),
                ("Q : SAUVEGARDER & QUITTER", (200, 200, 200))
            ]
        curr_y = SCREEN_HEIGHT // 2 + 20
        for text, color in lines:
            line_surf = font_small.render(text, True, color)
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, curr_y))
            surface.blit(line_surf, line_rect)
            curr_y += 35 # Espace entre les lignes

def setup_new_game(self, difficulty_name):
    config = DIFFICULTIES[difficulty_name]
    # On génère le nombre de mines dynamiquement selon la plage
    min_m, max_m = config["mine_range"]
    nb_mines = random.randint(min_m, max_m)
    # On crée la grille avec ce nombre aléatoire
    self.grid = Grid(config["rows"], config["cols"], nb_mines)
    print(f"Nouvelle partie {difficulty_name} lancée avec {nb_mines} mines.")