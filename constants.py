# --- WINDOW SETTINGS ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE_Y_POS = 80  # La hauteur du titre par rapport au haut
# --- GRID & LAYOUT ---
# On garde ton décalage de 160px pour laisser de la place au titre/chrono
HEADER_HEIGHT = 160 
GRID_OFFSET_Y = HEADER_HEIGHT 
MARGIN = 2 # Espace entre les cases
CELL_SIZE = 32  # Ou la taille que tu souhaites
# --- COLORS (RGB) ---
COLOR_BG = (15, 15, 20)           # Bleu très sombre
COLOR_ACCENT = (0, 255, 127)      # Vert néon
COLOR_TEXT = (240, 240, 240)      # Blanc cassé
# Palette Matrix / Terminal
COLOR_BG_DARK = (5, 5, 5)        # Noir profond
COLOR_MATRIX_GREEN = (0, 255, 65) # Vert digital néon
COLOR_HOVER_GREEN = (0, 60, 0)    # Vert très sombre pour l'effet de survol
C_BLACK = (5, 5, 5)            # Fond noir profond
C_GREEN_NEON = (0, 255, 65)    # Vert Matrix
C_GREEN_DARK = (0, 40, 0)      # Vert sombre (pour le hover)
C_LOCKED_GREY = (30, 30, 30)   # Gris pour bouton désactivé
 # --- COULEURS MATRIX ---
C_GREEN = (0, 255, 65)
C_DARK_GREEN = (0, 150, 40)
# Couleurs des boutons (pour ui_elements.py)
COLOR_BTN = (40, 40, 50)
COLOR_BTN_HOVER = (60, 60, 75)

# Couleurs des cases (pour renderer.py)
C_HIDDEN    = (70, 80, 100)       # Case fermée
C_REVEALED  = (200, 205, 215)     # Case vide révélée
C_MINE_BG   = (220, 60, 60)       # Fond rouge mine
C_FLAG      = (240, 180, 30)      # Jaune drapeau
C_BORDER_LT = (110, 125, 150)     # Bordure 3D claire
C_BORDER_DK = (20, 25, 35)        # Bordure 3D sombre
# --- NUMBER COLORS ---
NUMBER_COLORS = {
    1: (80, 130, 255), 2: (50, 200, 100), 3: (240, 80, 80),
    4: (130, 70, 200), 5: (220, 100, 40), 6: (60, 210, 210),
    7: (230, 50, 130), 8: (160, 160, 160)
}

# --- DIFFICULTY SETTINGS ---
# Note : on garde le cell_size ici car il change selon la difficulté !
# Configuration des difficultés : (Lignes, Colonnes, (Mines_Min, Mines_Max))
DIFFICULTIES = {
    "EASY": {
        "rows": 9, 
        "cols": 9, 
        "mine_range": (8, 12)  # Entre 8 et 12 mines aléatoirement
    },
    "MEDIUM": {
        "rows": 16, 
        "cols": 16, 
        "mine_range": (35, 45) # Entre 35 et 45 mines aléatoirement
    },
    "HARD": {
        "rows": 16, 
        "cols": 30, 
        "mine_range": (90, 105) # Entre 90 et 105 mines aléatoirement
    }
}

# --- ASSETS & FONTS ---
FONT_CUSTOM = "fonts/Digital-7/digital-7.ttf"
TITLE_FONT_SIZE = 70
DEFAULT_PLAYER_NAME = "INVITÉ"