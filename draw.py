from game_runner import *


class Draw:
    def __init__(self, fps_clock, display_surf, basic_font):
        self.fps_clock = fps_clock
        self.display_surf = display_surf
        self.basic_font = basic_font

    def draw_score(self, score):
        score_surf = self.basic_font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 120, 10)
        self.display_surf.blit(score_surf, score_rect)

    def draw_worm(self, worm_coords):
        for coord in worm_coords:
            x = coord['x'] * CELL_SIZE
            y = coord['y'] * CELL_SIZE
            worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display_surf, DARK_GREEN, worm_segment_rect)
            worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
            pygame.draw.rect(self.display_surf, GREEN, worm_inner_segment_rect)

    def draw_apple(self, coord):
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display_surf, RED, apple_rect)

    def draw_grid(self, ):
        # draw vertical lines
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.display_surf, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        # draw horizontal lines
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.display_surf, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw_press_key_msg(self, ):
        press_key_surf = self.basic_font.render('Press a key to play.', True, DARK_GRAY)
        press_key_rect = press_key_surf.get_rect()
        press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
        self.display_surf.blit(press_key_surf, press_key_rect)
