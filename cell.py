import pygame

# --- Taille d'une case en pixels ---
CELL_SIZE = 40

# --- Espace entre les cases pour qu'elles ne se touchent pas ---
MARGIN = 2

# --- Hauteur de la barre d'en-tête en haut de la fenêtre ---
HEADER_H = 80

# --- Couleurs au format RGB (Rouge, Vert, Bleu), chaque valeur entre 0 et 255 ---
C_HIDDEN    = (70,  80, 100)   # case non révélée (gris-bleu)
C_REVEALED  = (200, 205, 215)  # case révélée (gris clair)
C_MINE_BG   = (220,  60,  60)  # fond d'une mine explosée (rouge)
C_FLAG      = (240, 180,  30)  # couleur du drapeau (jaune)
C_BORDER_LT = (110, 125, 150)  # bordure claire (côtés haut et gauche) pour l'effet 3D
C_BORDER_DK = (20,   25,  35)  # bordure sombre (côtés bas et droite) pour l'effet 3D

# --- Couleur de chaque chiffre (1 à 8) affiché sur une case révélée ---
NUMBER_COLORS = {
    1: (80,  130, 255),  # bleu
    2: (50,  200, 100),  # vert
    3: (240,  80,  80),  # rouge
    4: (130,  70, 200),  # violet
    5: (220, 100,  40),  # orange
    6: (60,  210, 210),  # cyan
    7: (230,  50, 130),  # rose
    8: (160, 160, 160),  # gris
}


class Cell:
    # --- Le constructeur est appelé automatiquement à la création de chaque case ---
    def __init__(self, row: int, col: int):
        self.row            = row      # numéro de ligne dans la grille
        self.col            = col      # numéro de colonne dans la grille
        self.is_mine        = False    # True si cette case contient une mine
        self.revealed       = False    # True si le joueur a cliqué dessus
        self.flagged        = False    # True si le joueur a posé un drapeau
        self.neighbor_count = 0        # nombre de mines dans les 8 cases voisines

    # --- Révèle la case, sauf si elle a un drapeau (protection contre les faux clics) ---
    def reveal(self):
        if not self.flagged:
            self.revealed = True

    # --- Pose le drapeau si la case n'en a pas, le retire sinon (fonctionne comme un interrupteur) ---
    def toggle_flag(self):
        if not self.revealed:              # on ne peut pas flagguer une case déjà découverte
            self.flagged = not self.flagged

    # --- Dessine la case sur l'écran selon son état actuel ---
    def draw(self, surface, font_num, font_icon):

        # Calcule la position en pixels à partir du numéro de ligne/colonne
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE + HEADER_H  # + HEADER_H pour sauter la barre du haut

        # Crée le rectangle de la case en appliquant la marge pour espacer les cases
        rect = pygame.Rect(
            x + MARGIN,
            y + MARGIN,
            CELL_SIZE - 2 * MARGIN,
            CELL_SIZE - 2 * MARGIN
        )

        if self.revealed:
            if self.is_mine:
                # Case révélée qui est une mine : fond rouge avec une étoile
                pygame.draw.rect(surface, C_MINE_BG, rect, border_radius=4)
                txt = font_icon.render("*", True, (255, 255, 255))
                surface.blit(txt, txt.get_rect(center=rect.center))
            else:
                # Case révélée sans mine : fond gris clair
                pygame.draw.rect(surface, C_REVEALED, rect, border_radius=4)

                # Si des mines sont présentes autour, on affiche leur nombre en couleur
                if self.neighbor_count > 0:
                    color = NUMBER_COLORS.get(self.neighbor_count, (0, 0, 0))
                    txt = font_num.render(str(self.neighbor_count), True, color)
                    surface.blit(txt, txt.get_rect(center=rect.center))

        else:
            # Case non révélée : fond gris-bleu avec un effet 3D sur les bords
            pygame.draw.rect(surface, C_HIDDEN, rect, border_radius=4)

            # Bordures claires en haut et à gauche → effet "relief surélevé"
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.topright, 2)
            pygame.draw.line(surface, C_BORDER_LT, rect.topleft, rect.bottomleft, 2)

            # Bordures sombres en bas et à droite → renforce l'effet 3D
            pygame.draw.line(surface, C_BORDER_DK, rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(surface, C_BORDER_DK, rect.topright, rect.bottomright, 2)

            # Si un drapeau est posé, on affiche un drapeau au centre
            if self.flagged:
                txt = font_icon.render("🚩", True, C_FLAG)
                surface.blit(txt, txt.get_rect(center=rect.center))
