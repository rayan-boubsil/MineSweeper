from Button import Button
from Settings import *

class ModeSelectionScreen:
    """Original game modes selection."""
    def __init__(self, manager):
        self.manager = manager
        # Defining some original modes
        self.buttons = [
            Button(100, 200, 280, 80, "CLASSIQUE", lambda: print("Mode: Classique")),
            Button(420, 200, 280, 80, "MINES MOUVANTES", lambda: print("Mode: Mines Mouvantes")),
            Button(100, 320, 280, 80, "CONTRE LA MONTRE", lambda: print("Mode: Contre la Montre")),
            Button(420, 320, 280, 80, "CHIFFRES CACHÉS", lambda: print("Mode: Chiffres Cachés")),
            Button(300, 480, 200, 50, "BACK", lambda: self.manager.set_state("MAIN"))
        ]

    def draw(self, surface):
        surface.fill(COLOR_BG)
        self.manager.draw_header(surface, "SELECTION DU MODE")
        for b in self.buttons:
            b.draw(surface)