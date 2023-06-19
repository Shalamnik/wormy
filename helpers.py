import random


def get_random_location(width: int, height: int) -> dict:
    return {'x': random.randint(0, width - 1), 'y': random.randint(0, height - 1)}
