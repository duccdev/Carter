from curses.ascii import isdigit
from datetime import timedelta
import string


def parseDuration(duration: str) -> timedelta:
    total_seconds = 0

    tokens = list(duration)
    num = ""
    unit = ""
    for token in tokens:
        if token.isdigit() and not unit:
            num += token
        elif token.isalpha() and not unit:
            unit = token

            match unit:
                case "d":
                    total_seconds += int(num) * (24 * (60 * 60))
                case "h":
                    total_seconds += int(num) * (60 * 60)
                case "m":
                    total_seconds += int(num) * 60
                case "s":
                    total_seconds += int(num)
                case _:
                    raise ValueError(f"unknown unit '{unit}'")

            unit = ""
            num = ""
        else:
            raise ValueError(f"unexpected token '{token}'")

    if num and not unit:
        raise ValueError("expected unit")

    return timedelta(seconds=total_seconds)
