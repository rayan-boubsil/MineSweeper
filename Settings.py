# --- Dimensions de la fenêtre ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
# --- Palette de Couleurs (Format RGB) ---
COLOR_BG = (15, 15, 20)          # Bleu très sombre
COLOR_ACCENT = (0, 255, 127)      # Vert néon (Spring Green)
COLOR_TEXT = (240, 240, 240)      # Blanc cassé
COLOR_BTN = (40, 40, 50)          # Gris bleuté
COLOR_BTN_HOVER = (60, 60, 75)    # Gris bleuté clair (survol)
# --- Paramètres du Démineur ---
DIFFICULTIES = {
    "EASY": {
        "rows": 9,
        "cols": 9,
        "mines": 10,
        "cell_size": 40
    },
    "MEDIUM": {
        "rows": 16,
        "cols": 16,
        "mines": 40,
        "cell_size": 30
    },
    "HARD": {
        "rows": 16,
        "cols": 30,
        "mines": 99,
        "cell_size": 25
    }
}