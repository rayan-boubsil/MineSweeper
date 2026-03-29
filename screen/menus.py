import pygame
import os
import random
from constants import *
from display.ui_elements import Button
from manager.AudioManager import AudioManager

class MenuManager:
    def __init__(self, manager):
        self.manager = manager
        self.current_view = "MAIN" 
        self.buttons = []
        self.is_typing = False
        self.new_player_input = ""
        self.setup_main_menu()
        self.audio = AudioManager()
        self.audio.start_music("assets/sound_music_menu.ogg")
    # --- UTILITAIRES ---
    def _create_buttons(self, button_data):
        """Utilitaire pour créer une liste de boutons rapidement."""
        self.buttons = [Button(*data) for data in button_data]


    def _start_game(self, diff_key):
        """
        Starts a new game with the chosen difficulty and player name.
        Generates a random number of mines based on the difficulty range.
        """
        # 1. On récupère les paramètres de base (rows, cols, mine_range)
        config = DIFFICULTIES[diff_key].copy()
        # 2. On génère le nombre de mines aléatoire (La fameuse fourchette !)
        min_m, max_m = config["mine_range"]
        nb_mines = random.randint(min_m, max_m)
        # 3. On ajoute les infos nécessaires pour l'objet Game
        config.update({"name": self.manager.current_player_name, "difficulty": diff_key,"mines": nb_mines})
        # 4. On lance la partie
        self.manager.set_state("GAME", config)

    # --- CONFIGURATION DES VUES ---
    def setup_main_menu(self):
        self.current_view = "MAIN"
        bx = (SCREEN_WIDTH - 250) // 2
        name = self.manager.current_player_name
        has_prof = (name != DEFAULT_PLAYER_NAME)
        self._create_buttons([
            (bx, 150, 250, 40, f"PROFIL: {name}", self.setup_profile_menu),
            (bx, 220, 250, 50, "REPRENDRE", self.manager.load_existing_game),
            (bx, 290, 250, 50, "NOUVELLE PARTIE", self.setup_difficulty_menu if has_prof else None),
            (bx, 360, 250, 50, "SCORES", self.setup_scores_menu),
            (bx, 430, 250, 50, "QUITTER", self.manager.quit_game)
        ])
        for b in self.buttons:
            if b.text == "NOUVELLE PARTIE": b.active = has_prof
        self._check_save_visibility()

    def setup_difficulty_menu(self):
        self.current_view = "DIFFICULTY"
        bx = (SCREEN_WIDTH - 250) // 2
        self._create_buttons([
            (bx, 220, 250, 50, "FACILE", lambda: self._start_game("EASY")),
            (bx, 290, 250, 50, "INTERMEDIAIRE", lambda: self._start_game("MEDIUM")),
            (bx, 360, 250, 50, "EXPERT", lambda: self._start_game("HARD")),
            (bx, 450, 250, 50, "RETOUR", self.setup_main_menu)
        ])

    def setup_profile_menu(self):
        self.current_view = "PROFILES"
        self.buttons = []
        bx, y = (SCREEN_WIDTH - 300) // 2, 150
        for name in self.manager.profile_manager.get_list():
            self.buttons.append(Button(bx, y, 240, 40, name, lambda n=name: self.handle_profile_action("SELECT", n)))
            self.buttons.append(Button(bx + 250, y, 50, 40, "X", lambda n=name: self.handle_profile_action("DELETE", n)))
            y += 50
        self.buttons.append(Button(bx, y + 20, 300, 45, "CREER UN JOUEUR", self._start_typing))
        self.buttons.append(Button(bx, 500, 300, 45, "RETOUR", self.setup_main_menu))

    def setup_scores_menu(self):
        self.current_view = "SCORES"
        self.buttons = [Button((SCREEN_WIDTH - 250)//2, 520, 250, 50, "RETOUR", self.setup_main_menu)]

    # --- LOGIQUE & EVENTS ---
    def handle_profile_action(self, action, name):
        if action == "SELECT":
            self.manager.current_player_name = name
            self.setup_main_menu()
        elif action == "DELETE":
            if self.manager.profile_manager.delete(name):
                if self.manager.current_player_name == name: self.manager.current_player_name = "INVITÉ"
                self.setup_profile_menu()

    def _check_save_visibility(self):
        has_save = self.manager.save_manager.has_save(self.manager.current_player_name)
        for b in self.buttons:
            if b.text == "REPRENDRE": b.visible = has_save

    def _start_typing(self):
        self.is_typing, self.new_player_input = True, ""

    def handle_events(self, event):
        if self.is_typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.new_player_input:
                    self.manager.profile_manager.create(self.new_player_input)
                    self.manager.current_player_name = self.new_player_input
                    self.is_typing = False
                    self.setup_profile_menu()
                elif event.key == pygame.K_BACKSPACE: self.new_player_input = self.new_player_input[:-1]
                elif len(self.new_player_input) < 12 and event.unicode.isalnum():
                    self.new_player_input += event.unicode.upper()
            return 
        for b in self.buttons:
            if b.handle_event(event): self.manager.audio.play_sfx("click")

    def update(self, mouse_pos):
        if not pygame.mixer.music.get_busy():
            self.audio.start_music("assets/sound_music_menu.ogg")
        if not self.is_typing:
            for b in self.buttons: b.check_hover(mouse_pos)

    def draw(self, surface):
        titles = {"MAIN": "MINESWEEPER", "DIFFICULTY": "DIFFICULTE", "SCORES": "TOP SCORES", "PROFILES": "PROFILS"}
        self.manager.draw_header(surface, titles.get(self.current_view, ""))
        for b in self.buttons: b.draw(surface)
        if self.current_view == "SCORES": self.draw_score_list(surface)
        if self.is_typing: self._draw_typing_overlay(surface)

    def _draw_typing_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 250, 400, 120)
        pygame.draw.rect(surface, (40, 40, 45), rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_ACCENT, rect, 3, border_radius=10)
        font = pygame.font.SysFont("Arial", 22, bold=True)
        surface.blit(font.render("NOM DU NOUVEAU JOUEUR :", True, (255, 255, 255)), (rect.x + 20, rect.y + 20))
        surface.blit(font.render(self.new_player_input + "_", True, COLOR_ACCENT), (rect.x + 20, rect.y + 65))

    def draw_score_list(self, surface):
        f_cat = pygame.font.SysFont("Verdana", 20, bold=True)
        f_sub = pygame.font.SysFont("Verdana", 14, bold=True)
        f_score = pygame.font.SysFont("Consolas", 14)
        cols = {"EASY": SCREEN_WIDTH//6 + 20, "MEDIUM": SCREEN_WIDTH//2, "HARD": (5*SCREEN_WIDTH)//6 - 20}
        for cat, x in cols.items():
            data = self.manager.score_manager.scores.get(cat, {"history": [], "best": None})
            # Titre & Record
            surface.blit(f_cat.render(cat, True, COLOR_ACCENT), f_cat.render(cat, True, COLOR_ACCENT).get_rect(center=(x, 170)))
            surface.blit(f_sub.render("🏆 RECORD 🏆", True, (255, 215, 0)), f_sub.render("🏆 RECORD 🏆", True, (255, 215, 0)).get_rect(center=(x, 210)))
            best = data["best"]
            best_txt = f"{best['name'][:8]} - {best['time']}s" if best else "--- Aucun ---"
            surface.blit(f_score.render(best_txt, True, (255, 215, 0)), f_score.render(best_txt, True, (255, 215, 0)).get_rect(center=(x, 235)))
            # Historique
            surface.blit(f_sub.render("HISTORIQUE", True, (180, 180, 180)), f_sub.render("HISTORIQUE", True, (180, 180, 180)).get_rect(center=(x, 280)))
            y = 305
            for entry in data["history"]:
                c = (100, 255, 100) if "(WIN)" in entry['name'] else (255, 100, 100)
                name = entry['name'].replace("(WIN)","").replace("(LOST)","")[:8]
                txt = f"{name:<8} {entry['time']:>3}s"
                surface.blit(f_score.render(txt, True, c), f_score.render(txt, True, c).get_rect(center=(x, y)))
                y += 22
    def refresh_buttons(self):
        """
        Vérifie l'existence d'une sauvegarde et active/désactive le bouton 'Reprendre'.
        """
        # 1. On vérifie si le fichier existe (adapte le nom du fichier à ton projet)
        save_path = "savegame.json" 
        has_save = os.path.exists(save_path)
        # 2. On cherche le bouton "Reprendre" dans ta liste de boutons
        if "RESUME" in self.buttons:
            self.buttons["RESUME"].enabled = has_save
            if not has_save:
                self.buttons["RESUME"].alpha = 100 # Plus transparent
            else:
                self.buttons["RESUME"].alpha = 255 # Opacité normale