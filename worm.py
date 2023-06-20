from random import randint
from typing import Union

from apple import Apple
from variables import (
    CELL_HEIGHT,
    CELL_WIDTH,
    UP,
    DOWN,
    LEFT,
    RIGHT
)


class Worm:
    HEAD_IDX = 0

    def __init__(self):
        # Set a random start point
        start_x = randint(5, CELL_WIDTH - 6)
        start_y = randint(5, CELL_HEIGHT - 6)
        self.coords = [
            {'x': start_x, 'y': start_y},
            {'x': start_x - 1, 'y': start_y},
            {'x': start_x - 2, 'y': start_y}
        ]

    def get_coords(self, direction: str, apple_: Apple) -> Union[list, None]:
        if (
                self.coords[self.HEAD_IDX]['x'] == -1 or
                self.coords[self.HEAD_IDX]['x'] == CELL_WIDTH or
                self.coords[self.HEAD_IDX]['y'] == -1 or
                self.coords[self.HEAD_IDX]['y'] == CELL_HEIGHT
        ):
            return
        for worm_body in self.coords[1:]:
            if (
                    worm_body['x'] == self.coords[self.HEAD_IDX]['x'] and
                    worm_body['y'] == self.coords[self.HEAD_IDX]['y']
            ):
                return

        # check if worm has eaten an apple_
        if (
                self.coords[self.HEAD_IDX]['x'] == apple_.coords['x'] and
                self.coords[self.HEAD_IDX]['y'] == apple_.coords['y']
        ):
            # don't remove worm's tail segment
            # set a new apple_ somewhere
            apple_.set_random_location()
        else:
            # remove worm's tail segment
            del self.coords[-1]

        # move the worm by adding a segment in the direction it is moving
        new_head = {}
        if direction == UP:
            new_head = {
                'x': self.coords[self.HEAD_IDX]['x'],
                'y': self.coords[self.HEAD_IDX]['y'] - 1
            }
        elif direction == DOWN:
            new_head = {
                'x': self.coords[self.HEAD_IDX]['x'],
                'y': self.coords[self.HEAD_IDX]['y'] + 1
            }
        elif direction == LEFT:
            new_head = {
                'x': self.coords[self.HEAD_IDX]['x'] - 1,
                'y': self.coords[self.HEAD_IDX]['y']
            }
        elif direction == RIGHT:
            new_head = {
                'x': self.coords[self.HEAD_IDX]['x'] + 1,
                'y': self.coords[self.HEAD_IDX]['y']
            }

        self.coords.insert(0, new_head)

        return self.coords
