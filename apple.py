from random import randint

from variables import CELL_WIDTH, CELL_HEIGHT


class Apple:
    def __init__(self):
        self.coords = {}
        self.set_random_location()

    def set_random_location(self):
        self.coords = {
            'x': randint(0, CELL_WIDTH - 1),
            'y': randint(0, CELL_HEIGHT - 1)
        }
