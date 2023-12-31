import sys
from random import choice
from time import time

import pygame
from pygame.locals import (
    K_UP,
    KEYUP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a, K_w, K_s, K_d
)

from apple import Apple
from db_worker import DBWorker
from draw import (
    Draw,
    BG_COLOR,
    WHITE,
    DARK_GREEN,
    GREEN
)
from variables import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    UP,
    DOWN,
    RIGHT,
    LEFT,
    GAME_TIME,
    WIN_SCORE,
)
from worm import Worm


class Game:
    def __init__(self):
        pygame.init()
        self.FPS_CLOCK = pygame.time.Clock()
        self.DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
        self.draw = Draw(self.FPS_CLOCK, self.DISPLAY_SURF, self.BASIC_FONT)
        pygame.display.set_caption('Wormy')

        self.user_name = ''
        self.user_score = 0
        self.db_worker = DBWorker()

    def run(self):
        self.show_start_screen()
        self.user_name = self.show_user_input()
        while True:
            self.run_game()
            self.db_worker.record_user_score(self.user_name, self.user_score)
            self.show_finish_screen()

    def run_game(self):
        direction = choice([UP, DOWN, LEFT, RIGHT])

        _apple = Apple()
        _worm = Worm()

        start_time = time()

        while True:
            time_left = time() - start_time
            if time_left > GAME_TIME:
                return

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                        direction = LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                        direction = RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                        direction = UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                        direction = DOWN
                    elif event.key == K_ESCAPE:
                        self.terminate()

            worm_coords = _worm.get_coords(direction, _apple)
            if not worm_coords:
                return

            user_score = len(worm_coords) - 3
            self.user_score = user_score

            self.DISPLAY_SURF.fill(BG_COLOR)

            self.draw.draw_grid()
            self.draw.draw_worm(worm_coords)
            self.draw.draw_apple(_apple)
            self.draw.draw_score(user_score)
            self.draw.draw_timer(time_left)
            self.draw.draw_game_rules()

            pygame.display.update()

            self.FPS_CLOCK.tick(FPS)

    def is_key_pressed(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.terminate()

        key_up_events = pygame.event.get(KEYUP)
        if len(key_up_events) == 0:
            return None
        if key_up_events[0].key == K_ESCAPE:
            self.terminate()
        return key_up_events[0].key

    def show_start_screen(self):
        title_font = pygame.font.Font('freesansbold.ttf', 100)
        title_surf1 = title_font.render('Wormy!', True, WHITE, DARK_GREEN)
        title_surf2 = title_font.render('Wormy!', True, GREEN)

        degrees1 = 0
        degrees2 = 0
        while True:
            self.DISPLAY_SURF.fill(BG_COLOR)
            rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
            rotated_rect1 = rotated_surf1.get_rect()
            rotated_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            self.DISPLAY_SURF.blit(rotated_surf1, rotated_rect1)

            rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
            rotated_rect2 = rotated_surf2.get_rect()
            rotated_rect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            self.DISPLAY_SURF.blit(rotated_surf2, rotated_rect2)

            self.draw.draw_press_key_msg()

            if self.is_key_pressed():
                pygame.event.get()
                return

            pygame.display.update()

            self.FPS_CLOCK.tick(FPS)

            degrees1 += 3
            degrees2 += 7

    def show_user_input(self):
        self.DISPLAY_SURF.fill(BG_COLOR)

        is_input_filled = False
        user_text = ''

        input_rect = pygame.Rect(200, 200, 200, 60)

        while True:
            if is_input_filled:
                return user_text.rstrip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        is_input_filled = True

                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

            pygame.draw.rect(self.DISPLAY_SURF, DARK_GREEN, input_rect)

            text_surface = self.BASIC_FONT.render(user_text, True, WHITE)
            text_hint = self.BASIC_FONT.render('Input your name:', True, WHITE)

            self.draw.draw_game_rules()
            self.draw.draw_press_enter_start()
            # render at position stated in arguments
            self.DISPLAY_SURF.blit(text_surface, (input_rect.x + 5, input_rect.y + 35))
            self.DISPLAY_SURF.blit(text_hint, (input_rect.x + 20, input_rect.y + 5))

            pygame.display.flip()

            self.FPS_CLOCK.tick(FPS)

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def show_finish_screen(self):
        self.DISPLAY_SURF.fill(BG_COLOR)

        if self.user_score >= WIN_SCORE:
            self.show_win_screen()
        else:
            self.show_game_over_screen()

        self.show_user_scores()

        self.draw.draw_press_key_msg()
        pygame.display.update()
        pygame.time.wait(500)

        self.is_key_pressed()

        while True:
            if self.is_key_pressed():
                pygame.event.get()
                return

    def show_win_screen(self):
        font = pygame.font.Font('freesansbold.ttf', 60)
        you_surf = font.render('You', True, WHITE)
        win_surf = font.render('Won!', True, WHITE)
        you_rect = you_surf.get_rect()
        win_rect = win_surf.get_rect()
        you_rect.midtop = (WINDOW_WIDTH / 2, 10)
        win_rect.midtop = (WINDOW_WIDTH / 2, you_rect.height + 10 + 25)

        self.DISPLAY_SURF.blit(you_surf, you_rect)
        self.DISPLAY_SURF.blit(win_surf, win_rect)

    def show_game_over_screen(self):
        font = pygame.font.Font('freesansbold.ttf', 60)
        game_surf = font.render('Game', True, WHITE)
        over_surf = font.render('Over', True, WHITE)
        game_rect = game_surf.get_rect()
        over_rect = over_surf.get_rect()
        game_rect.midtop = (WINDOW_WIDTH / 2, 10)
        over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

        self.DISPLAY_SURF.blit(game_surf, game_rect)
        self.DISPLAY_SURF.blit(over_surf, over_rect)

    def show_user_scores(self):
        margin_top = 20

        user_score = f'{self.user_name}, your score: {self.user_score}'
        user_top_result = self.db_worker.get_top_result(self.user_name)
        user_top_result = f'Your top result: {user_top_result}'

        top_header = f'Top 5 users:'
        top_user_scores = self.db_worker.get_top_users()

        self.render_center_text(user_score, margin_top)
        margin_top += 20
        self.render_center_text(user_top_result, margin_top)
        margin_top += 40
        self.render_center_text(top_header, margin_top)
        margin_top += 20

        for user in top_user_scores:
            self.render_center_text(f"{user['name']}: {user['score']}", margin_top)
            margin_top += 20

    def render_center_text(self, text: str, margin_top: int = 0):
        score_font = pygame.font.Font('freesansbold.ttf', 18)
        score_surf = score_font.render(
            text,
            True,
            WHITE
        )
        score_rect = score_surf.get_rect()
        score_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + margin_top)

        self.DISPLAY_SURF.blit(score_surf, score_rect)
