import pygame
import sys
from ScoreManager import ScoreManager
from Scoreboard import ScoreboardScreen
from AudioManager import AudioManager 
from DifficultyMenu import DifficultyMenu
from MainMenu import MainMenu
from Settings import *

class MainLoop:
    """Le contrôleur principal qui fait tourner le jeu et gère les écrans."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper 3D")
        self.clock = pygame.time.Clock()
        # 1. --- États et Données ---
        self.state = "MAIN" 
        self.current_config = None 
        # 2. --- Animation du Titre (À METTRE ICI !) ---
        self.intro_done = False # <--- On l'ajoute bien ici
        self.title_index = 0
        self.last_title_update = pygame.time.get_ticks()
        self.type_speed = 100  
        # 3. --- Dictionnaire de navigation ---
        self.state_names = {
            "MAIN": "MENU PRINCIPAL",
            "DIFFICULTY": "CHOIX DE DIFFICULTÉ",
            "SCORES": "MEILLEURS SCORES"
        }
        # 4. --- Systèmes (Outils) ---
        self.score_manager = ScoreManager() 
        self.audio = AudioManager() 
        # 5. --- Écrans (Interfaces - EN DERNIER) ---
        # Maintenant qu'intro_done existe, on peut créer les menus sans risque
        self.main_menu = MainMenu(self)
        self.score_screen = ScoreboardScreen(self)
        self.difficulty_screen = DifficultyMenu(self)

    # --- Fonctions Utilitaires ---
    def set_state(self, new_state):
        """Change l'écran actif."""
        self.state = new_state

    def quit_game(self):
        """Ferme proprement le programme."""
        pygame.quit()
        sys.exit()

    def draw_header(self, surface, text):
        now = pygame.time.get_ticks()
        # --- ÉTAPE 1 : ANIMATION D'ÉCRITURE (Intro) ---
        if not self.intro_done:
            if self.title_index < len(text):
                if now - self.last_title_update > self.type_speed:
                    self.title_index += 1
                    self.last_title_update = now
            else:
                self.intro_done = True
        else:
            self.title_index = len(text)
        # --- ÉTAPE 2 : LOGIQUE DU "SCANNER" (Toutes les 3 secondes) ---
        # On calcule quelle lettre doit briller
        # 3000ms = cycle de 3 secondes
        cycle_time = 3000 
        progress = now % cycle_time 
        # On fait parcourir l'index de 0 à la fin du texte pendant la première seconde
        # Les 2 secondes restantes, rien ne brille (pause)
        glow_index = -1
        if progress < 1000: # La vague dure 1 seconde
            glow_index = int((progress / 1000) * len(text))
        # --- ÉTAPE 3 : DESSIN ---
        try:
            font = pygame.font.Font(FONT_CUSTOM, TITLE_FONT_SIZE)
        except:
            font = pygame.font.SysFont("Impact", TITLE_FONT_SIZE)
        pos_x, pos_y = 75, TITLE_Y_POS
        # 1. Dessiner tout le texte affiché (Couleur de base)
        text_to_show = text[:self.title_index]
        surf_base = font.render(text_to_show, True, COLOR_ACCENT)
        surface.blit(surf_base, (pos_x, pos_y))
        # 2. Dessiner la lettre qui "brille" (seulement si l'intro est finie)
        if self.intro_done and 0 <= glow_index < len(text):
            char = text[glow_index]
            # Couleur très vive (Blanc ou Vert très clair)
            surf_glow = font.render(char, True, (200, 255, 200)) 
            # Calculer la position X de cette lettre précise
            # On mesure la largeur de ce qui précède la lettre
            offset_x = font.size(text[:glow_index])[0]
            surface.blit(surf_glow, (pos_x + offset_x, pos_y))

    def set_state(self, new_state):
        # 1. On vérifie si on revient du jeu vers le menu
        # Si l'état actuel est "GAME" et qu'on passe à "MAIN"
        if self.state == "GAME" and new_state == "MAIN":
            self.intro_done = False   # On autorise à nouveau l'animation
            self.title_index = 0      # On repart de zéro lettre
            self.last_title_update = pygame.time.get_ticks()
        # 2. On change l'état
        self.state = new_state

    # --- Cœur du programme (Logic & Rendering) ---
    def update(self, mouse_pos):
        """Met à jour la logique des boutons (survol)."""
        if self.state == "MAIN":
            self.main_menu.update(mouse_pos)
        elif self.state == "DIFFICULTY":
            self.difficulty_screen.update(mouse_pos)
        elif self.state == "SCORES":
            self.score_screen.btn_back.update(mouse_pos)

    def draw(self):
        """Dessine l'interface selon l'état actuel."""
        self.screen.fill(COLOR_BG) # 1. Fond de base
        # --- 2. NOUVEAU : INDICATEUR DE POSITION (Haut à Droite) ---
        # On ne l'affiche que si on n'est PAS en train de jouer
        if self.state != "GAME":
            # On récupère le nom depuis le dictionnaire (ex: "MENU PRINCIPAL")
            current_name = self.state_names.get(self.state, "")
            if current_name:
                font_nav = pygame.font.SysFont("Verdana", 14, bold=True)
                nav_surf = font_nav.render(current_name, True, COLOR_ACCENT)
                # Position : à 30px du bord droit et 25px du haut
                nav_x = SCREEN_WIDTH - nav_surf.get_width() - 30
                nav_y = 25
                self.screen.blit(nav_surf, (nav_x, nav_y))
                # Trait horizontal décoratif
                line_y = nav_y + nav_surf.get_height() + 5
                pygame.draw.line(self.screen, COLOR_ACCENT, (nav_x, line_y), (SCREEN_WIDTH - 30, line_y), 2)
        # --- 3. DESSIN DES ÉCRANS ---
        if self.state == "MAIN":
            self.main_menu.draw(self.screen)
        elif self.state == "DIFFICULTY":
            self.difficulty_screen.draw(self.screen)
        elif self.state == "SCORES":
            self.score_screen.draw(self.screen)
        elif self.state == "GAME":
            self.draw_header(self.screen, "IN GAME...")
        pygame.display.flip() # 4. Rafraîchissement visuel

    def run(self):
        """Boucle infinie du jeu."""
        while True:
            mouse_pos = pygame.mouse.get_pos()
            # 1. Gestion des événements (Clavier / Souris)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.audio.play_sfx("click") 
                # Délégation des clics aux écrans
                if self.state == "MAIN":
                    self.main_menu.handle_events(event)
                elif self.state == "DIFFICULTY":
                    self.difficulty_screen.handle_events(event)
                elif self.state == "SCORES":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.score_screen.btn_back.handle_click()
            # 2. Mise à jour de la logique
            self.update(mouse_pos)
            # 3. Dessin
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = MainLoop()
    app.run()