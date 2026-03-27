import sys
import pygame
from grid import Grid
from cell import CELL_SIZE, HEADER_H

# --- Grid size in number of cells ---
COLS  = 16
ROWS  = 16
MINES = 40

# --- Window size calculated automatically in pixels ---
WIN_W = COLS * CELL_SIZE             # width = number of columns x cell size
WIN_H = ROWS * CELL_SIZE + HEADER_H  # height = grid + header bar

# --- Number of times the screen redraws per second ---
FPS = 60

# --- General interface colors ---
C_BG     = (30,  30,  40)   # window background (very dark gray)
C_HEADER = (20,  22,  32)   # header bar background (even darker)
C_WIN    = (50,  200, 100)  # victory message color (green)
C_LOSE   = (220,  60,  60)  # defeat message color (red)


class Game:

    # --- The three possible states of a game ---
    STATE_PLAYING = "playing"   # game is ongoing
    STATE_WIN     = "win"       # player won
    STATE_LOSE    = "lose"      # player lost

    # --- Constructor initializes pygame, the window and all game elements ---
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Minesweeper")

        # Create the window with the correct dimensions
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))

        # Internal clock that keeps the game running at 60 FPS
        self.clock  = pygame.time.Clock()

        # Text fonts of different sizes for the interface
        self.font_num  = pygame.font.SysFont("consolas", 22, bold=True)  # numbers on cells
        self.font_ui   = pygame.font.SysFont("consolas", 18, bold=True)  # header text
        self.font_big  = pygame.font.SysFont("consolas", 32, bold=True)  # end-of-game message
        self.font_icon = self.font_num                                    # icons (F, ?, *)

        # Create the empty game grid
        self.grid        = Grid(ROWS, COLS, MINES)

        # Initial game state
        self.state       = self.STATE_PLAYING

        # Start time (in milliseconds) used by the timer
        self.start_ticks = pygame.time.get_ticks()

        # Elapsed time displayed in seconds
        self.elapsed     = 0

        # Rectangle of the Restart button (updated on every draw)
        self.reset_rect  = pygame.Rect(0, 0, 0, 0)

    # --- Main loop: runs forever at 60 FPS ---
    def run(self):
        while True:
            self._handle_events()   # 1. read player actions
            self._update()          # 2. update the timer
            self._draw()            # 3. redraw the screen
            self.clock.tick(FPS)    # 4. wait to stay under 60 FPS

    # --- Reads and processes all events since the last frame ---
    def _handle_events(self):
        for event in pygame.event.get():

            # Close button -> quit cleanly
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # R key -> start a new game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._reset()

            # Mouse click (left or right)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos   # click coordinates in pixels

                # If the click lands on the Restart button -> reset
                if self.reset_rect.collidepoint(mx, my):
                    self._reset()
                    return

                # If the click is inside the grid and the game is ongoing
                if my >= HEADER_H and self.state == self.STATE_PLAYING:

                    # Convert pixel coordinates to row/column numbers
                    col = mx // CELL_SIZE
                    row = (my - HEADER_H) // CELL_SIZE

                    # Make sure the click is within the grid boundaries
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if event.button == 1:     # left click -> reveal cell
                            self._left_click(row, col)
                        elif event.button == 3:   # right click -> cycle flag / ? / nothing
                            self.grid.toggle_flag(row, col)

    # --- Handles a left click on cell (row, col) ---
    def _left_click(self, row: int, col: int):

        # On the very first click, place the mines now
        # (guarantees the player never lands on a mine from the start)
        if not self.grid._initialized:
            self.grid._place_mines(row, col)
            self.start_ticks = pygame.time.get_ticks()   # start the timer

        cell = self.grid.cells[row][col]

        # If the cell is already marked or revealed, do nothing
        if cell.flagged or cell.revealed or cell.questioned:
            return

        # Reveal the cell (and recursively propagate if it is empty)
        self.grid.reveal(row, col)

        # Check the result after revealing
        if cell.is_mine:
            self.grid.reveal_all_mines()    # show all mines
            self.state = self.STATE_LOSE    # game over
        elif self.grid.is_victory():
            self.state = self.STATE_WIN     # player wins

    # --- Updates the timer (only while the game is ongoing) ---
    def _update(self):
        if self.state == self.STATE_PLAYING:
            # get_ticks() returns ms elapsed since pygame started
            # Subtract the start time and divide by 1000 -> seconds
            self.elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000

    # --- Redraws the entire screen every frame ---
    def _draw(self):
        self.screen.fill(C_BG)                                      # clear the screen
        self._draw_header()                                         # draw the top bar
        self.grid.draw(self.screen, self.font_num, self.font_icon)  # draw all cells
        if self.state != self.STATE_PLAYING:
            self._draw_overlay()        # show end-of-game message if the game is over
        pygame.display.flip()           # push everything drawn to the screen

    # --- Draws the header bar (remaining mines, timer, Restart button) ---
    def _draw_header(self):

        # Dark background of the header
        pygame.draw.rect(self.screen, C_HEADER, (0, 0, WIN_W, HEADER_H))

        # Remaining mines = total - number of flags placed (displayed on the left)
        remaining = MINES - self.grid.flags_placed
        mines_txt = self.font_ui.render(f"Mines: {remaining:>3}", True, (240, 100, 100))
        self.screen.blit(mines_txt, (16, HEADER_H // 2 - mines_txt.get_height() // 2))

        # Timer displayed on the right
        time_txt = self.font_ui.render(f"Time: {self.elapsed:>4}s", True, (180, 210, 255))
        self.screen.blit(time_txt, (WIN_W - time_txt.get_width() - 16,
                                    HEADER_H // 2 - time_txt.get_height() // 2))

        # Centered Restart button with a rounded background
        btn_txt = self.font_ui.render(" Restart (R) ", True, (220, 220, 220))
        self.reset_rect = btn_txt.get_rect(center=(WIN_W // 2, HEADER_H // 2))
        pygame.draw.rect(self.screen, (50, 60, 80),
                         self.reset_rect.inflate(8, 6), border_radius=6)
        pygame.draw.rect(self.screen, (90, 110, 140),
                         self.reset_rect.inflate(8, 6), 2, border_radius=6)
        self.screen.blit(btn_txt, self.reset_rect)

    # --- Displays a semi-transparent overlay with the end-of-game message ---
    def _draw_overlay(self):

        # Transparent surface at 160/255 opacity laid over the grid
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Choose the message and color based on the game state
        msg, color = ("YOU WIN!", C_WIN) if self.state == self.STATE_WIN \
                     else ("GAME OVER!", C_LOSE)

        # Display the main message at the center of the screen
        txt = self.font_big.render(msg, True, color)
        self.screen.blit(txt, txt.get_rect(center=(WIN_W // 2, WIN_H // 2 - 20)))

        # Display the restart instruction just below
        sub = self.font_ui.render("Press R to play again", True, (200, 200, 200))
        self.screen.blit(sub, sub.get_rect(center=(WIN_W // 2, WIN_H // 2 + 30)))

    # --- Resets the game (new grid, initial state, timer back to zero) ---
    def _reset(self):
        self.grid        = Grid(ROWS, COLS, MINES)
        self.state       = self.STATE_PLAYING
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed     = 0
