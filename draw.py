import pygame

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

    def draw_score(self, score: int, window_width: int):
        score_surf = self.basic_font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (window_width - 120, 10)
        self.display_surf.blit(score_surf, score_rect)

    def draw_worm(self, worm_coords, cell_size: int):
        for coord in worm_coords:
            x = coord['x'] * cell_size
            y = coord['y'] * cell_size
            worm_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(self.display_surf, DARK_GREEN, worm_segment_rect)
            worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, cell_size - 8, cell_size - 8)
            pygame.draw.rect(self.display_surf, GREEN, worm_inner_segment_rect)

    def draw_apple(self, coord: dict, cell_size: int):
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        apple_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(self.display_surf, RED, apple_rect)

    def draw_grid(
            self,
            window_width: int,
            window_height: int,
            cell_size: int,
    ):
        # draw vertical lines
        for x in range(0, window_width, cell_size):
            pygame.draw.line(self.display_surf, DARK_GRAY, (x, 0), (x, window_height))
        # draw horizontal lines
        for y in range(0, window_height, cell_size):
            pygame.draw.line(self.display_surf, DARK_GRAY, (0, y), (window_width, y))

    def draw_press_key_msg(
            self,
            window_width: int,
            window_height: int
    ):
        press_key_surf = self.basic_font.render('Press a key to play.', True, DARK_GRAY)
        press_key_rect = press_key_surf.get_rect()
        press_key_rect.topleft = (window_width - 200, window_height - 30)
        self.display_surf.blit(press_key_surf, press_key_rect)