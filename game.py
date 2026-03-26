import sys
import pygame
from grid import Grid
from cell import CELL_SIZE, HEADER_H

# --- Taille de la grille en nombre de cases ---
COLS  = 16
ROWS  = 16
MINES = 40

# --- Taille de la fenêtre calculée automatiquement en pixels ---
WIN_W = COLS * CELL_SIZE           # largeur = nombre de colonnes × taille d'une case
WIN_H = ROWS * CELL_SIZE + HEADER_H  # hauteur = grille + barre d'en-tête

# --- Nombre de fois que l'écran se redessine par seconde ---
FPS = 60

# --- Couleurs générales de l'interface ---
C_BG     = (30,  30,  40)   # fond de la fenêtre (gris très sombre)
C_HEADER = (20,  22,  32)   # fond de la barre d'en-tête (encore plus sombre)
C_WIN    = (50,  200, 100)  # couleur du message de victoire (vert)
C_LOSE   = (220,  60,  60)  # couleur du message de défaite (rouge)


class Game:

    # --- Les trois états possibles d'une partie ---
    STATE_PLAYING = "playing"   # partie en cours
    STATE_WIN     = "win"       # joueur a gagné
    STATE_LOSE    = "lose"      # joueur a perdu

    # --- Le constructeur initialise pygame, la fenêtre et tous les éléments du jeu ---
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Demineur")

        # Crée la fenêtre avec les bonnes dimensions
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))

        # Horloge interne qui régule la vitesse du jeu à 60 FPS
        self.clock  = pygame.time.Clock()

        # Polices de texte de différentes tailles pour l'interface
        self.font_num  = pygame.font.SysFont("consolas", 22, bold=True)  # chiffres sur les cases
        self.font_ui   = pygame.font.SysFont("consolas", 18, bold=True)  # texte de l'en-tête
        self.font_big  = pygame.font.SysFont("consolas", 32, bold=True)  # message de fin de partie
        self.font_icon = self.font_num                                    # icônes (F, ?, *)

        # Création de la grille de jeu vide
        self.grid        = Grid(ROWS, COLS, MINES)

        # État initial de la partie
        self.state       = self.STATE_PLAYING

        # Temps de départ (en millisecondes) pour le chronomètre
        self.start_ticks = pygame.time.get_ticks()

        # Temps écoulé affiché en secondes
        self.elapsed     = 0

        # Rectangle du bouton Restart (mis à jour à chaque dessin)
        self.reset_rect  = pygame.Rect(0, 0, 0, 0)

    # --- Boucle principale : tourne indéfiniment à 60 FPS ---
    def run(self):
        while True:
            self._handle_events()   # 1. lire les actions du joueur
            self._update()          # 2. mettre à jour le chronomètre
            self._draw()            # 3. redessiner l'écran
            self.clock.tick(FPS)    # 4. attendre pour ne pas dépasser 60 FPS

    # --- Lit et traite tous les événements survenus depuis le dernier tour ---
    def _handle_events(self):
        for event in pygame.event.get():

            # Croix de fermeture → on quitte proprement
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Touche R → relancer une nouvelle partie
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._reset()

            # Clic de souris (gauche ou droit)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos   # coordonnées du clic en pixels

                # Si le clic tombe sur le bouton Restart → relancer
                if self.reset_rect.collidepoint(mx, my):
                    self._reset()
                    return

                # Si le clic est dans la grille et que la partie est en cours
                if my >= HEADER_H and self.state == self.STATE_PLAYING:

                    # Convertit les pixels en numéro de ligne/colonne
                    col = mx // CELL_SIZE
                    row = (my - HEADER_H) // CELL_SIZE

                    # Vérifie que le clic est bien dans les limites de la grille
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if event.button == 1:     # clic gauche → révéler la case
                            self._left_click(row, col)
                        elif event.button == 3:   # clic droit → cycle drapeau / ? / rien
                            self.grid.toggle_flag(row, col)

    # --- Gère un clic gauche sur la case (row, col) ---
    def _left_click(self, row: int, col: int):

        # Au tout premier clic, on place les mines maintenant
        # (garantit que le joueur ne tombe jamais sur une mine dès le départ)
        if not self.grid._initialized:
            self.grid._place_mines(row, col)
            self.start_ticks = pygame.time.get_ticks()   # démarre le chronomètre

        cell = self.grid.cells[row][col]

        # Si la case est déjà marquée ou révélée, on ne fait rien
        if cell.flagged or cell.revealed or cell.questioned:
            return

        # Révèle la case (et propage récursivement si elle est vide)
        self.grid.reveal(row, col)

        # Vérifie le résultat après la révélation
        if cell.is_mine:
            self.grid.reveal_all_mines()    # montre toutes les mines
            self.state = self.STATE_LOSE    # partie perdue
        elif self.grid.is_victory():
            self.state = self.STATE_WIN     # partie gagnée

    # --- Met à jour le chronomètre (uniquement si la partie est en cours) ---
    def _update(self):
        if self.state == self.STATE_PLAYING:
            # get_ticks() retourne les ms écoulées depuis le lancement de pygame
            # On soustrait le temps de départ et on divise par 1000 → secondes
            self.elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000

    # --- Redessine tout l'écran à chaque tour de boucle ---
    def _draw(self):
        self.screen.fill(C_BG)                                      # efface l'écran
        self._draw_header()                                         # dessine la barre du haut
        self.grid.draw(self.screen, self.font_num, self.font_icon)  # dessine toutes les cases
        if self.state != self.STATE_PLAYING:
            self._draw_overlay()        # affiche le message de fin si la partie est terminée
        pygame.display.flip()           # envoie tout ce qu'on a dessiné à l'écran

    # --- Dessine la barre d'en-tête (mines restantes, chrono, bouton Restart) ---
    def _draw_header(self):

        # Fond sombre de l'en-tête
        pygame.draw.rect(self.screen, C_HEADER, (0, 0, WIN_W, HEADER_H))

        # Mines restantes = total − nombre de drapeaux posés (affiché à gauche)
        remaining = MINES - self.grid.flags_placed
        mines_txt = self.font_ui.render(f"Mines: {remaining:>3}", True, (240, 100, 100))
        self.screen.blit(mines_txt, (16, HEADER_H // 2 - mines_txt.get_height() // 2))

        # Chronomètre affiché à droite
        time_txt = self.font_ui.render(f"Temps: {self.elapsed:>4}s", True, (180, 210, 255))
        self.screen.blit(time_txt, (WIN_W - time_txt.get_width() - 16,
                                    HEADER_H // 2 - time_txt.get_height() // 2))

        # Bouton Restart centré avec un fond arrondi
        btn_txt = self.font_ui.render(" Restart (R) ", True, (220, 220, 220))
        self.reset_rect = btn_txt.get_rect(center=(WIN_W // 2, HEADER_H // 2))
        pygame.draw.rect(self.screen, (50, 60, 80),
                         self.reset_rect.inflate(8, 6), border_radius=6)
        pygame.draw.rect(self.screen, (90, 110, 140),
                         self.reset_rect.inflate(8, 6), 2, border_radius=6)
        self.screen.blit(btn_txt, self.reset_rect)

    # --- Affiche un écran semi-transparent avec le message de fin de partie ---
    def _draw_overlay(self):

        # Surface transparente à 160/255 d'opacité posée par-dessus la grille
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Choix du message et de la couleur selon l'état de la partie
        msg, color = ("VICTOIRE !", C_WIN) if self.state == self.STATE_WIN \
                     else ("PERDU !", C_LOSE)

        # Affiche le message principal au centre de l'écran
        txt = self.font_big.render(msg, True, color)
        self.screen.blit(txt, txt.get_rect(center=(WIN_W // 2, WIN_H // 2 - 20)))

        # Affiche l'instruction pour recommencer juste en dessous
        sub = self.font_ui.render("Appuie sur R pour recommencer", True, (200, 200, 200))
        self.screen.blit(sub, sub.get_rect(center=(WIN_W // 2, WIN_H // 2 + 30)))

    # --- Remet le jeu à zéro (nouvelle grille, état initial, chrono remis à 0) ---
    def _reset(self):
        self.grid        = Grid(ROWS, COLS, MINES)
        self.state       = self.STATE_PLAYING
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed     = 0
