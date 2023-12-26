import secrets


def randint(min: int, max: int) -> int:
    return secrets.randbelow(max) + min
