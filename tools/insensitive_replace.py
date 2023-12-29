import re


def insensitive_replace(text: str, old: str, new: str) -> str:
    return re.compile(re.escape(old), re.IGNORECASE).sub(new, text)
