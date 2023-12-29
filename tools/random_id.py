from . import random
import string


def random_id(length: int = 16) -> str:
    return "".join(
        random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length)
    )
