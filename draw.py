import pygame
from apple import Apple

from variables import (
    WIN_SCORE,
    GAME_TIME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CELL_SIZE
)

# R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
DARK_GRAY = (40, 40, 40)
BG_COLOR = BLACK


class Draw:
    def __init__(self, fps_clock, display_surf, basic_font):
        self.fps_clock = fps_clock
        self.display_surf = display_surf
        self.basic_font = basic_font

    def draw_score(self, score: int):
        score_surf = self.basic_font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 120, 10)
        self.display_surf.blit(score_surf, score_rect)

    def draw_timer(self, secs: float):
        score_surf = self.basic_font.render(f'Time: {int(secs)}', True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 120, 40)
        self.display_surf.blit(score_surf, score_rect)

    def draw_game_rules(self):
        score_surf = self.basic_font.render(
            f'Eat >= {WIN_SCORE} apple(s) to Win before "Time: {GAME_TIME}"',
            True,
            WHITE
        )
        score_rect = score_surf.get_rect()
        score_rect.midtop = (WINDOW_WIDTH / 2, 20)
        self.display_surf.blit(score_surf, score_rect)

    def draw_press_enter_start(self):
        score_surf = self.basic_font.render(
            'Press "Enter" to start',
            True,
            WHITE
        )
        score_rect = score_surf.get_rect()
        score_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)
        self.display_surf.blit(score_surf, score_rect)

    def draw_worm(self, worm_coords):
        for coord in worm_coords:
            x = coord['x'] * CELL_SIZE
            y = coord['y'] * CELL_SIZE
            worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display_surf, DARK_GREEN, worm_segment_rect)
            worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
            pygame.draw.rect(self.display_surf, GREEN, worm_inner_segment_rect)

    def draw_apple(self, apple_: Apple):
        x = apple_.coords['x'] * CELL_SIZE
        y = apple_.coords['y'] * CELL_SIZE
        apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display_surf, RED, apple_rect)

    def draw_grid(self):
        # draw vertical lines
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.display_surf, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        # draw horizontal lines
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.display_surf, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw_press_key_msg(self):
        press_key_surf = self.basic_font.render('Press a key to play', True, WHITE)
        press_key_rect = press_key_surf.get_rect()
        press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
        self.display_surf.blit(press_key_surf, press_key_rect)
