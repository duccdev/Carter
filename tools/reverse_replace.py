def reverseReplace(string: str, old: str, new: str, count: int) -> str:
    return new.join(string.rsplit(old, count))
