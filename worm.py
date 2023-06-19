from helpers import random
from game_runner import *

from typing import Union


class Worm:
    HEAD_IDX = 0

    def __init__(self):
        # Set a random start point
        start_x = random.randint(5, CELL_WIDTH - 6)
        start_y = random.randint(5, CELL_HEIGHT - 6)
        self.worm_coords = [
            {'x': start_x, 'y': start_y},
            {'x': start_x - 1, 'y': start_y},
            {'x': start_x - 2, 'y': start_y}
        ]

    def get_coords(self, direction: str, apple: dict) -> Union[list, None]:
        if (
                self.worm_coords[self.HEAD_IDX]['x'] == -1 or
                self.worm_coords[self.HEAD_IDX]['x'] == CELL_WIDTH or
                self.worm_coords[self.HEAD_IDX]['y'] == -1 or
                self.worm_coords[self.HEAD_IDX]['y'] == CELL_HEIGHT
        ):
            return
        for worm_body in self.worm_coords[1:]:
            if (
                    worm_body['x'] == self.worm_coords[self.HEAD_IDX]['x'] and
                    worm_body['y'] == self.worm_coords[self.HEAD_IDX]['y']
            ):
                return

        # check if worm has eaten an apple
        if (
                self.worm_coords[self.HEAD_IDX]['x'] == apple['x'] and
                self.worm_coords[self.HEAD_IDX]['y'] == apple['y']
        ):
            # don't remove worm's tail segment
            # set a new apple somewhere
            apple = get_random_location(CELL_WIDTH, CELL_HEIGHT)
        else:
            # remove worm's tail segment
            del self.worm_coords[-1]

        # move the worm by adding a segment in the direction it is moving
        new_head = {}
        if direction == UP:
            new_head = {
                'x': self.worm_coords[self.HEAD_IDX]['x'],
                'y': self.worm_coords[self.HEAD_IDX]['y'] - 1
            }
        elif direction == DOWN:
            new_head = {
                'x': self.worm_coords[self.HEAD_IDX]['x'],
                'y': self.worm_coords[self.HEAD_IDX]['y'] + 1
            }
        elif direction == LEFT:
            new_head = {
                'x': self.worm_coords[self.HEAD_IDX]['x'] - 1,
                'y': self.worm_coords[self.HEAD_IDX]['y']
            }
        elif direction == RIGHT:
            new_head = {
                'x': self.worm_coords[self.HEAD_IDX]['x'] + 1,
                'y': self.worm_coords[self.HEAD_IDX]['y']
            }

        self.worm_coords.insert(0, new_head)

        return self.worm_coords
