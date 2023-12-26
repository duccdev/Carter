from . import randint


def randbool() -> bool:
    return randint(1, 2) > 1
