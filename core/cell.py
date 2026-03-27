class Cell:
    """
    Représente une case unique de la grille.
    Contient uniquement les données d'état (Modèle).
    """
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_mine = False
        self.revealed = False
        # marker_state : 0 = Rien, 1 = Drapeau, 2 = Point d'interrogation
        self.marker_state = 0  
        self.neighbor_count = 0

    def reveal(self):
        """Révèle la case si elle n'est pas marquée par un drapeau."""
        if self.marker_state == 0:
            self.revealed = True

    def toggle_flag(self):
        """
        Alterne l'état du marqueur (cycle entre Vide, Drapeau et Question).
        Appelé par Grid.toggle_flag()
        """
        if not self.revealed:
            # Cycle : 0 -> 1 -> 2 -> 0
            self.marker_state = (self.marker_state + 1) % 3