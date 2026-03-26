import sys
import pygame
from grid import Grid
from cell import CELL_SIZE, HEADER_H

COLS  = 16
ROWS  = 16
MINES = 40

WIN_W = COLS * CELL_SIZE
WIN_H = ROWS * CELL_SIZE + HEADER_H
FPS   = 60

C_BG     = (30,  30,  40)
C_HEADER = (20,  22,  32)
C_WIN    = (50,  200, 100)
C_LOSE   = (220,  60,  60)


class Game:
    STATE_PLAYING = "playing"
    STATE_WIN     = "win"
    STATE_LOSE    = "lose"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Demineur")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock  = pygame.time.Clock()

        self.font_num  = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_ui   = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_big  = pygame.font.SysFont("consolas", 32, bold=True)
        self.font_icon = self.font_num

        self.grid        = Grid(ROWS, COLS, MINES)
        self.state       = self.STATE_PLAYING
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed     = 0
        self.reset_rect  = pygame.Rect(0, 0, 0, 0)

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._reset()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if self.reset_rect.collidepoint(mx, my):
                    self._reset()
                    return
                if my >= HEADER_H and self.state == self.STATE_PLAYING:
                    col = mx // CELL_SIZE
                    row = (my - HEADER_H) // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if event.button == 1:
                            self._left_click(row, col)
                        elif event.button == 3:
                            self.grid.toggle_flag(row, col)

    def _left_click(self, row: int, col: int):
        if not self.grid._initialized:
            self.grid._place_mines(row, col)
            self.start_ticks = pygame.time.get_ticks()

        cell = self.grid.cells[row][col]
        if cell.flagged or cell.revealed:
            return

        self.grid.reveal(row, col)

        if cell.is_mine:
            self.grid.reveal_all_mines()
            self.state = self.STATE_LOSE
        elif self.grid.is_victory():
            self.state = self.STATE_WIN

    def _update(self):
        if self.state == self.STATE_PLAYING:
            self.elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000

    def _draw(self):
        self.screen.fill(C_BG)
        self._draw_header()
        self.grid.draw(self.screen, self.font_num, self.font_icon)
        if self.state != self.STATE_PLAYING:
            self._draw_overlay()
        pygame.display.flip()

    def _draw_header(self):
        pygame.draw.rect(self.screen, C_HEADER, (0, 0, WIN_W, HEADER_H))

        remaining = MINES - self.grid.flags_placed
        mines_txt = self.font_ui.render(f"Mines: {remaining:>3}", True, (240, 100, 100))
        self.screen.blit(mines_txt, (16, HEADER_H // 2 - mines_txt.get_height() // 2))

        time_txt = self.font_ui.render(f"Temps: {self.elapsed:>4}s", True, (180, 210, 255))
        self.screen.blit(time_txt, (WIN_W - time_txt.get_width() - 16,
                                    HEADER_H // 2 - time_txt.get_height() // 2))

        btn_txt = self.font_ui.render(" Restart (R) ", True, (220, 220, 220))
        self.reset_rect = btn_txt.get_rect(center=(WIN_W // 2, HEADER_H // 2))
        pygame.draw.rect(self.screen, (50, 60, 80),
                         self.reset_rect.inflate(8, 6), border_radius=6)
        pygame.draw.rect(self.screen, (90, 110, 140),
                         self.reset_rect.inflate(8, 6), 2, border_radius=6)
        self.screen.blit(btn_txt, self.reset_rect)

    def _draw_overlay(self):
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        msg, color = ("VICTOIRE !", C_WIN) if self.state == self.STATE_WIN \
                     else ("PERDU !", C_LOSE)

        txt = self.font_big.render(msg, True, color)
        self.screen.blit(txt, txt.get_rect(center=(WIN_W // 2, WIN_H // 2 - 20)))

        sub = self.font_ui.render("Appuie sur R pour recommencer", True, (200, 200, 200))
        self.screen.blit(sub, sub.get_rect(center=(WIN_W // 2, WIN_H // 2 + 30)))

    def _reset(self):
        self.grid        = Grid(ROWS, COLS, MINES)
        self.state       = self.STATE_PLAYING
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed     = 0
