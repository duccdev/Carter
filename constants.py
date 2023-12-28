from config import BOT_PREFIX

ERROR = "i fucked up LMAO :sob:"

HELP_PAGE = [
    {
        "name": ":smirk: NSFW",
        "content": f"- Fetch images/GIFs using `{BOT_PREFIX}nsfw`",
    },
    {
        "name": ":slight_smile: Fun commands",
        "content": f"""
- Get a random cat using `{BOT_PREFIX}cat`
- Get a random dog using `{BOT_PREFIX}dog`
- Get a random (useless!) fact using `{BOT_PREFIX}fact`
- Get a random meme using `{BOT_PREFIX}meme`
    """,
    },
    {
        "name": ":game_die: Games",
        "content": f"""
- Get the leaderboard of a game using `{BOT_PREFIX}leaderboard`
- Roll the dice using `{BOT_PREFIX}dice`
- Get a would you rather question using `{BOT_PREFIX}wyr`
- Play a cup game using `{BOT_PREFIX}cups`
- Play rock paper scissors using `{BOT_PREFIX}rps`
    """,
    },
    {
        "name": ":gear: Other",
        "content": f"""
- Show this help page using `{BOT_PREFIX}help`
- Start a server poll using `{BOT_PREFIX}poll` if permitted
- Check bot ping using `{BOT_PREFIX}ping`
- Chat with the bot by pinging/replying to it
    """,
    },
]

NSFW_HELP_PAGE = [
    {"name": "Usage", "content": f"`{BOT_PREFIX}nsfw <category> <type>`"},
    {"name": "Example", "content": f"`{BOT_PREFIX}nsfw blowjob gif`"},
    {
        "name": "Categories and types",
        "content": f"""
- `anal` (`gif`)
- `blowjob` (`gif`)
- `cum` (`gif`)
- `fuck` (`gif`)
- `neko` (`gif`, `img`)
- `pussylick` (`gif`)
- `solo` (`gif`)
- `solo_male` (`gif`)
- `threesome_fff` (`gif`)
- `threesome_ffm` (`gif`)
- `threesome_mmf` (`gif`)
- `yaoi` (`gif`)
- `yuri` (`gif`)
    """,
    },
]

POLL_HELP_PAGE = [
    {"name": "Usage", "content": f"`{BOT_PREFIX}poll <channel> <poll> <emojis>`"},
    {
        "name": "Example",
        "content": f'`{BOT_PREFIX}poll #polls "should i set a minecraft server up for this server?" :x: :white_check_mark:`',
    },
]

LEADERBOARD_HELP_PAGE = [
    {"name": "Usage", "content": "f`{BOT_PREFIX}leaderboard <game>`"},
    {"name": "Example", "content": f"`{BOT_PREFIX}leaderboard cups`"},
    {"name": "Supported games", "content": f"- `cups`\n- `rps`"},
]

NSFW_WRONG_CHANNEL = "ayo wtf you doin? take that shit to the nsfw channels!"
NSFW_NOT_FOUND = (
    "Category and/or type not found, guess you gotta jerk off to something else!"
)

LEADERBOARD_NO_PLAYERS = (
    "yeah uh there are no players currently on the leaderboard :skull_crossbones:"
)

NON_OWNER_INTERACTION = "MF THIS ISNT YOURS"
CUPS_TIMEOUT = "bro you really took THAT long to press a FUCKING BUTTON??"

ROCK = 0
PAPER = 1
SCISSORS = 2

RPS_TIMEOUT = "fucker stop overthinking what to choose"
RPS_TIE = "oop its a tie"
RPS_WIN = "soo YOU WON WOOOO"
RPS_LOSE = "soo you lost lmaooooo"
