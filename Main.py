import pygame
import sys
import os

# --- Imports des Managers (Nouveaux emplacements) ---
from manager.ScoreManager import ScoreManager
from manager.AudioManager import AudioManager
from manager.SaveManager import SaveManager
from manager.ProfileManager import ProfileManager

# --- Imports des Écrans (Tout est regroupé dans screen) ---
from screen.menus import MenuManager
from screen.game import Game

# --- Import des Constantes ---
from constants import *


class MainLoop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper 3D")
        self.clock = pygame.time.Clock()
        # 1. --- États et Données ---
        self.state = "MAIN"
        self.current_player_name = DEFAULT_PLAYER_NAME
        self.current_config = None
        # 2. --- Animation du Titre ---
        self.last_title_update = pygame.time.get_ticks()
        self.type_speed = 100
        self.title_index = 0
        self.intro_completed = False
        # 3. --- Chargement des Polices ---
        try:
            self.header_font = pygame.font.Font(FONT_CUSTOM, 50)
            # On ajoute les polices pour le renderer.py ici
            self.font_ui = pygame.font.SysFont("Arial", 24, bold=True)
            self.font_num = pygame.font.SysFont("Arial", 22, bold=True)
            self.font_icon = pygame.font.SysFont("Segoe UI Symbol", 22)
        except Exception as e:
            print(f"⚠️ Erreur polices : {e}")
            self.header_font = pygame.font.SysFont("Impact", 50)
            self.font_ui = pygame.font.SysFont("Arial", 24)
            self.font_num = pygame.font.SysFont("Arial", 22)
            self.font_icon = pygame.font.SysFont("Arial", 22)
        # 4. --- Dictionnaire de navigation ---
        self.state_names = {
            "MAIN": "MENU PRINCIPAL",
            "DIFFICULTY": "CHOIX DE DIFFICULTÉ",
            "SCORES": "MEILLEURS SCORES",
        }
        # 5. --- Systèmes (Managers) ---
        self.score_manager = ScoreManager()
        self.audio = AudioManager()
        self.profile_manager = ProfileManager(self)  # <-- Nouveau
        self.save_manager = SaveManager()  # On l'ajoute ici
        # 6. --- Écrans ---
        self.menu = MenuManager(self)
        self.game = None

    def set_state(self, new_state, config=None):
        """Change d'écran et gère l'initialisation."""
        self.state = new_state
        # Reset de l'animation d'écriture pour les menus
        if new_state != "GAME":
            self.intro_completed = False
            self.title_index = 0
            self.last_title_update = pygame.time.get_ticks()
        if new_state == "MAIN":
            self.menu.refresh_buttons()
        elif new_state == "GAME":
            if config:
                self.game = Game(self, config)
                self.game.player_name = self.current_player_name

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def load_existing_game(self):
        """Charge la partie en cours pour le profil actif."""
        player = self.current_player_name
        save_data = self.save_manager.load_game(player)
        if save_data:
            # 1. On change d'état vers "GAME" (ceci crée self.game)
            self.set_state("GAME", save_data["config"])
            # 2. ON CORRIGE ICI : On utilise self.game
            # Car c'est le nom que tu as défini dans set_state !
            self.game.apply_save_data(save_data)
            print(f"Partie de {player} reprise avec succès.")
        else:
            print(f"Erreur : Aucune sauvegarde valide pour {player}")
            self.menu.setup_main_menu()

    def get_existing_profiles(self):
        """Liste les noms des joueurs ayant une sauvegarde dans le dossier /saves."""
        if not os.path.exists("saves"):
            return []
        # On récupère les noms de fichiers sans l'extension .dat
        return [
            f.replace(".dat", "") for f in os.listdir("saves") if f.endswith(".dat")
        ]

    def update(self, mouse_pos):
        """Met à jour la logique des menus ou du jeu."""
        # Si on est dans n'un des états de menu, on update le MenuManager
        if self.state in ["MAIN", "DIFFICULTY", "SCORES"]:
            self.menu.update(mouse_pos)  # <--- LOGIQUE (Survol)
        elif self.state == "GAME" and self.game:
            self.game.update()  # <--- LOGIQUE (Chrono, etc.)

    def draw_header(self, surface, title_text):
        """Dessine le bandeau de titre en haut de l'écran."""
        # Fond du header
        pygame.draw.rect(surface, (20, 20, 25), (0, 0, SCREEN_WIDTH, 120))
        pygame.draw.line(surface, COLOR_ACCENT, (0, 120), (SCREEN_WIDTH, 120), 3)
        # Texte du titre
        title_surf = self.header_font.render(title_text, True, COLOR_ACCENT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title_surf, title_rect)

    def draw(self):
        """Dessine l'interface sur l'écran."""
        self.screen.fill(COLOR_BG)
        # Si on est dans un menu, on demande au MenuManager de dessiner
        if self.state in ["MAIN", "DIFFICULTY", "SCORES"]:
            self.menu.draw(self.screen)  # <--- DESSIN (Boutons, Titre)
        elif self.state == "GAME" and self.game:
            self.game.draw(self.screen)  # <--- DESSIN (Grille, HUD)
        pygame.display.flip()

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.audio.play_sfx("click")
                # Gestion des événements selon l'état
                if self.state == "GAME" and self.game:
                    self.game.handle_event(event)
                elif self.state in ["MAIN", "DIFFICULTY", "SCORES"]:
                    self.menu.handle_events(
                        event
                    )  # Un seul appel pour tous les menus !
            self.update(mouse_pos)
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    app = MainLoop()
    app.run()
