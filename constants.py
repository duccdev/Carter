ERROR = "i fucked up LMAO :sob:"

HELP_PAGE = [
    {"name": ":smirk: NSFW", "content": "- Fetch images/GIFs using `cb!nsfw`"},
    {
        "name": ":slight_smile: Fun commands",
        "content": """
- Get a random cat using `cb!cat`
- Get a random dog using `cb!dog`
- Get a random (useless!) fact using `cb!fact`
- Get a random meme using `cb!meme`
    """,
    },
    {
        "name": ":game_die: Games",
        "content": """
- Get the leaderboard of a game using `cb!leaderboard`
- Roll the dice using `cb!dice`
- Get a would you rather question using `cb!wyr`
- Play a cup game using `cb!cups`
    """,
    },
    {"name": ":gear: Other", "content": "- Show this help page using `cb!help`"},
]

NSFW_HELP_PAGE = [
    {"name": "Usage", "content": "`cb!nsfw <category> <type>`"},
    {"name": "Example", "content": "`cb!nsfw blowjob gif`"},
    {
        "name": "Categories and types",
        "content": """
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
    {"name": "Usage", "content": "`cb!poll <channel> <poll> <emojis>`"},
    {
        "name": "Example",
        "content": '`cb!poll #polls "should i set a minecraft server up for this server?" :x: :white_check_mark:`',
    },
]

LEADERBOARD_HELP_PAGE = [
    {"name": "Usage", "content": "`cb!leaderboard <game>`"},
    {"name": "Example", "content": "`cb!leaderboard cups`"},
    {"name": "Supported games", "content": "- `cups`"},
]

NSFW_WRONG_CHANNEL = "ayo wtf you doin? take that shit to the nsfw channels!"
NSFW_NOT_FOUND = (
    "Category and/or type not found, guess you gotta jerk off to something else!"
)

LEADERBOARD_NO_PLAYERS = (
    "yeah uh there are no players currently on the leaderboard :skull_crossbones:"
)

DUCC = 719562834295390299
