from subprocess import run
from discord import Embed, Color
from datetime import timedelta
import re, os


def parse_duration(duration: str) -> timedelta:
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


def ping() -> str:
    os.system("ping 1.1.1.1 -c 1 > /tmp/ping")

    with open("/tmp/ping") as fp:
        ping = fp.read().splitlines()[1]
        ping = ping[(ping.find("time=") + 5) :]

    os.remove("/tmp/ping")

    return ping


def create_embed(embed_template: dict):
    embed = Embed(title=embed_template.get("title", "Embed"), color=Color.random())

    if embed_template.get("description"):
        embed.description = embed_template["description"]

    if embed_template.get("footer"):
        embed.set_footer(text=embed_template["footer"])

    for field in embed_template.get("fields", []):
        embed.add_field(name=field["name"], value=field["content"], inline=False)

    return embed


def live_commit() -> tuple[str, str]:
    return (
        run(
            ["git", "log", "-n1", '--format="%h"'],
            capture_output=True,
            text=True,
        ).stdout.strip()[1:-1],
        run(
            ["git", "log", "-n1", '--format="%H"'],
            capture_output=True,
            text=True,
        ).stdout.strip()[1:-1],
    )


def reverse_replace(string: str, old: str, new: str, count: int) -> str:
    return new.join(string.rsplit(old, count))


def insensitive_replace(text: str, old: str, new: str) -> str:
    return re.compile(re.escape(old), re.IGNORECASE).sub(new, text)
