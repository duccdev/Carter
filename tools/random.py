import secrets, string

random = secrets.SystemRandom()


def id(length: int = 16) -> str:
    return "".join(
        random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length)
    )


choice = random.choice
randint = random.randint
