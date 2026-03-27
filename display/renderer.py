import pygame
from constants import *

class GameRenderer:
    def __init__(self):
        # On peut stocker ici des réglages par défaut si besoin
        pass

    def draw_cell(self, surface, cell, rect, font_num, font_icon):
        """Dessine une cellule individuelle selon son état logique."""
        if cell.revealed:
            if cell.is_mine:
                # Fond de mine et icône
                pygame.draw.rect(surface, C_MINE_BG, rect, border_radius=4)
                txt = font_icon.render("💣", True, (255, 255, 255))
                surface.blit(txt, txt.get_rect(center=rect.center))
            else:
                # Case vide révélée
                pygame.draw.rect(surface, C_REVEALED, rect, border_radius=4)
                if cell.neighbor_count > 0:
                    colors = {1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0)}
                    color = colors.get(cell.neighbor_count, (255, 255, 255))
                    txt = font_num.render(str(cell.neighbor_count), True, color)
                    surface.blit(txt, txt.get_rect(center=rect.center))
        else:
            # Case cachée avec effet de relief (beveled)
            pygame.draw.rect(surface, C_HIDDEN, rect, border_radius=4)
            # Bordures claires (haut/gauche)
            pygame.draw.line(surface, (120, 120, 120), rect.topleft, rect.topright, 2)
            pygame.draw.line(surface, (120, 120, 120), rect.topleft, rect.bottomleft, 2)
            # Bordures sombres (bas/droite)
            pygame.draw.line(surface, (30, 30, 30), rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(surface, (30, 30, 30), rect.topright, rect.bottomright, 2)
            # Dessin des marqueurs (Drapeau ou ?)
            if cell.marker_state == 1:
                txt = font_icon.render("🚩", True, C_FLAG)
                surface.blit(txt, txt.get_rect(center=rect.center))
            elif cell.marker_state == 2:
                txt = font_num.render("?", True, (255, 255, 255))
                surface.blit(txt, txt.get_rect(center=rect.center))

    def draw_grid(self, surface, grid, font_num, font_icon, cell_size):
        """Calcule les positions et dessine toute la grille."""
        grid_width = grid.cols * cell_size
        x_offset = (surface.get_width() - grid_width) // 2
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.cells[r][c]
                rect = pygame.Rect(
                    x_offset + c * cell_size, 
                    GRID_OFFSET_Y + r * cell_size, 
                    cell_size - 2, 
                    cell_size - 2
                )
                self.draw_cell(surface, cell, rect, font_num, font_icon)

    def draw_hud(self, surface, game, font_ui, font_icon):
        """Dessine les informations du haut (Chrono, Mines restantes)."""
        # Chrono
        timer_txt = font_ui.render(f"⏱️ {game.elapsed_time}s", True, (255, 255, 255))
        surface.blit(timer_txt, (20, 20))
        # Calcul des mines restantes (via la méthode get_flags_count() de grid)
        mines_left = game.grid.mines - game.grid.get_flags_count()
        mines_txt = font_ui.render(f"💣 {mines_left}", True, (255, 255, 255))
        surface.blit(mines_txt, (surface.get_width() - 150, 20))
        # Bouton Reset (le Smiley)
        pygame.draw.rect(surface, (200, 200, 200), game.reset_btn_rect, border_radius=8)
        status = "😵" if game.game_over else "😎" if game.won else "😊"
        res_txt = font_icon.render(status, True, (0, 0, 0))
        surface.blit(res_txt, res_txt.get_rect(center=game.reset_btn_rect.center))

    def draw_pause_overlay(self, surface, font_ui):
        """Affiche un écran de pause au look Matrix/Terminal."""
        # 1. Voile sombre transparent (On le garde, c'est parfait pour le contraste)
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) # Un peu plus sombre (200) pour faire ressortir le vert
        surface.blit(overlay, (0, 0))
        # 2. Texte "PAUSE" (Titre)
        font_pause = pygame.font.SysFont("Impact", 90)
        title = font_pause.render("PAUSE", True, C_GREEN)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, surface.get_height() // 3)))
        # 3. Instructions (Style Consolas/Terminal)
        instr_font = pygame.font.SysFont("Consolas", 22, bold=True)
        txt_resume = instr_font.render("> Pressez 'P' pour Reprendre", True, C_DARK_GREEN)
        # On met à jour le texte pour correspondre à ton nouveau handle_event (Menu principal)
        txt_menu = instr_font.render("> Pressez 'Q' pour Menu Principal", True, C_DARK_GREEN)
        surface.blit(txt_resume, txt_resume.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
        surface.blit(txt_menu, txt_menu.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 45)))
        # 4. LE PETIT PLUS : Bordure de l'écran
        pygame.draw.rect(surface, C_GREEN, (0, 0, surface.get_width(), surface.get_height()), 2)

    def draw_end_overlay(self, surface, won):
        """Draws the end game screen with instructions and theme colors."""
        # 1. Overlay semi-transparent
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        # Noir profond ou Vert très sombre
        bg_color = (0, 0, 0, 230) if not won else (0, 20, 0, 230)
        overlay.fill(bg_color)
        surface.blit(overlay, (0, 0))
        # 2. Titre Principal (Impact pour le côté imposant)
        title_text = "VICTOIRE !" if won else "GAME OVER"
        color = (0, 255, 65) if won else (255, 40, 40) # Vert Matrix ou Rouge Alerte
        font_end = pygame.font.SysFont("Impact", 90)
        txt = font_end.render(title_text, True, color)
        surface.blit(txt, txt.get_rect(center=(surface.get_width() // 2, 220)))
        # 3. Instructions (Style Terminal)
        # On utilise Consolas pour le look "informatique"
        font_instr = pygame.font.SysFont("Consolas", 22, bold=True)
        instr_text = "Appuyez sur [R] pour Rejouer  |  [Q] pour Menu Principal"
        # On utilise un vert plus doux pour ne pas voler la vedette au titre
        instr_surf = font_instr.render(instr_text, True, (0, 200, 50)) 
        surface.blit(instr_surf, instr_surf.get_rect(center=(surface.get_width() // 2, 330)))

    def draw_game_scene(self, surface, game):
        """Point d'entrée principal pour dessiner tout l'écran de jeu."""
        # On récupère les polices depuis le manager
        f_num = game.manager.font_num
        f_icon = game.manager.font_icon
        f_ui = game.manager.font_ui
        surface.fill(COLOR_BG)
        # Dessin de la grille (on passe la taille de cellule définie dans les constantes)
        self.draw_grid(surface, game.grid, f_num, f_icon, CELL_SIZE)
        # Dessin de l'interface
        self.draw_hud(surface, game, f_ui, f_icon)
        # Overlays
        if game.paused:
            self.draw_pause_overlay(surface, f_ui)
        elif game.game_over or game.won:
            self.draw_end_overlay(surface, game.won)