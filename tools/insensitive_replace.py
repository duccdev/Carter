import re


def insensitiveReplace(text: str, old: str, new: str) -> str:
    return re.compile(re.escape(old), re.IGNORECASE).sub(new, text)
