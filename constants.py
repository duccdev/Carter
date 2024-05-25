from config import BOT_PREFIX
import colors, tools.other, google.generativeai as genai

DUCC = 842457844724400142
SQD = 1077982815070728223

FACTS_ROUTE = "https://uselessfacts.jsph.pl/api/v2/facts/random"
CATS_ROUTE = "https://api.thecatapi.com/v1/images/search"
DOGS_ROUTE = "https://api.thedogapi.com/v1/images/search"
MEMES_ROUTE = "https://meme-api.com/gimme"
TRUTH_ROUTE = "https://api.truthordarebot.xyz/v1/truth"
DARE_ROUTE = "https://api.truthordarebot.xyz/api/dare"
WOULD_YOU_RATHER_ROUTE = "https://api.truthordarebot.xyz/api/wyr"
NEVER_HAVE_I_EVER_ROUTE = "https://api.truthordarebot.xyz/api/nhie"

LIVE_COMMIT_SHORT, LIVE_COMMIT_LONG = tools.other.live_commit()

LOG_PREFIX = f"[{colors.GREEN}Carter{colors.END}]"

HELP_PAGES = {
    "main": {
        "title": "❓ Help",
        "description": """
- 🙂 Fun
- 🎲 Games
- 🔨 Moderation
- 🤖 AI
- ⚙️ Other
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help main`",
    },
    "ai": {
        "title": "🤖 AI",
        "description": f"""
- Chat with the bot by pinging/replying to it
- Reset your AI conversation using `{BOT_PREFIX}ai-reset`
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help ai`",
    },
    "fun": {
        "title": "🙂 Fun",
        "description": f"""
- Get a random cat using `{BOT_PREFIX}cat`
- Get a random dog using `{BOT_PREFIX}dog`
- Get a random (useless!) fact using `{BOT_PREFIX}fact`
- Get a random meme using `{BOT_PREFIX}meme`
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help fun`",
    },
    "games": {
        "title": "🎲 Games",
        "description": f"""
- Get the leaderboard of a game using `{BOT_PREFIX}leaderboard`
- Roll the dice using `{BOT_PREFIX}dice`
- Play a cup game using `{BOT_PREFIX}cups`
- Play rock paper scissors using `{BOT_PREFIX}rps`
- Play RPS against other members using `{BOT_PREFIX}rps-pvp <other_member>`
- Play TicTacToe against other members using `{BOT_PREFIX}tictactoe <other_member>`
- Get a truth using `{BOT_PREFIX}truth` (read `{BOT_PREFIX}truth help`)
- Get a dare using `{BOT_PREFIX}dare` (read `{BOT_PREFIX}dare help`)
- Get a would you rather using `{BOT_PREFIX}wyr` (read `{BOT_PREFIX}wyr help`)
- Get a never have I ever using `{BOT_PREFIX}nhie` (read `{BOT_PREFIX}nhie help`)
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help games`",
    },
    "moderation": {
        "title": "🔨 Moderation",
        "description": f"""
- Ban a member using `{BOT_PREFIX}ban`
- Unban a member using `{BOT_PREFIX}unban`
- Kick a member using `{BOT_PREFIX}kick`
- Warn a member using `{BOT_PREFIX}warn`
- Read a member's warns using `{BOT_PREFIX}warns`
- Unwarn a member using `{BOT_PREFIX}unwarn`
- Time a member out using `{BOT_PREFIX}timeout`
- Remove a member's timeout using `{BOT_PREFIX}untimeout`
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help moderation`",
    },
    "other": {
        "title": "⚙️ Other",
        "description": f"""
- Show this help page using `{BOT_PREFIX}help`
- Start a server poll using `{BOT_PREFIX}poll` if permitted
- Check bot ping using `{BOT_PREFIX}ping`
- Know the contributors using `{BOT_PREFIX}contributors`
- Live Commit: **[{LIVE_COMMIT_SHORT}](https://github.com/duccybaka/Carter/commit/{LIVE_COMMIT_LONG})**
        """,
        "footer": f"Quickly access this page using `{BOT_PREFIX}help other`",
    },
}

TRUTH_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}truth`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}truth [rating]`"},
        {"name": "Example", "content": f"`{BOT_PREFIX}truth pg13`"},
        {
            "name": "Ratings",
            "content": """
- If no rating is specified, it will randomly choose `pg` or `pg13`
- `pg`
- `pg13`
- `r` (NSFW channels only)
            """,
        },
    ],
}

DARE_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}dare`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}dare [rating]`"},
        {"name": "Example", "content": f"`{BOT_PREFIX}dare pg13`"},
        {
            "name": "Ratings",
            "content": """
- If no rating is specified, it will randomly choose `pg` or `pg13`
- `pg`
- `pg13`
- `r` (NSFW channels only)
        """,
        },
    ],
}

WYR_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}wyr`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}wyr [rating]`"},
        {"name": "Example", "content": f"`{BOT_PREFIX}wyr pg13`"},
        {
            "name": "Ratings",
            "content": """
- If no rating is specified, it will randomly choose `pg` or `pg13`
- `pg`
- `pg13`
- `r` (NSFW channels only)
        """,
        },
    ],
}

NHIE_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}nhie`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}nhie [rating]`"},
        {"name": "Example", "content": f"`{BOT_PREFIX}nhie pg13`"},
        {
            "name": "Ratings",
            "content": """
- If no rating is specified, it will randomly choose `pg` or `pg13`
- `pg`
- `pg13`
- `r` (NSFW channels only)
        """,
        },
    ],
}

CONTRIBUTORS = {
    "title": "Contributors",
    "fields": [
        {
            "name": "Developers",
            "content": f"- <@{DUCC}> (Founder)\n- <@{SQD}> (AI dev, helper)",
        },
    ],
}

LEADERBOARD_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}leaderboard`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}leaderboard <game>`"},
        {"name": "Example", "content": f"`{BOT_PREFIX}leaderboard cups`"},
        {
            "name": "Supported games",
            "content": "- `cups`\n- `rps`\n- `rps-pvp`\n- `tictactoe`",
        },
        {"name": "Aliases", "content": f"- `{BOT_PREFIX}lb`"},
    ],
}

BAN_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}ban`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}ban <user> [reason]`"},
        {
            "name": "Examples",
            "content": f"""
- `{BOT_PREFIX}ban @amogustroll69 trolling`
- `{BOT_PREFIX}ban @amogustroll69`
        """,
        },
    ],
}

UNBAN_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}unban`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}unban <user>`"},
        {
            "name": "Example",
            "content": f"`{BOT_PREFIX}unban @amogustroll69`",
        },
    ],
}

KICK_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}kick`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}kick <user> [reason]`"},
        {
            "name": "Examples",
            "content": f"""
- `{BOT_PREFIX}kick @amogustroll69 trolling`
- `{BOT_PREFIX}kick @amogustroll69`
        """,
        },
    ],
}

WARN_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}warn`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}warn <user> <reason>`"},
        {
            "name": "Example",
            "content": f"`{BOT_PREFIX}warn @amogustroll69 sending nsfw in general`",
        },
    ],
}

WARNS_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}warns`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}warns <user>`"},
        {
            "name": "Example",
            "content": f"`{BOT_PREFIX}warns @amogustroll69`",
        },
    ],
}

UNWARN_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}warns`",
    "fields": [
        {"name": "Usage", "content": f"`{BOT_PREFIX}unwarn <user> <warn_id>`"},
        {
            "name": "Example",
            "content": f"`{BOT_PREFIX}unwarn @amogustroll69 NaFKsQvN`",
        },
    ],
}

TIMEOUT_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}timeout`",
    "fields": [
        {
            "name": "Usage",
            "content": f"`{BOT_PREFIX}timeout <user> <duration> [reason]`",
        },
        {
            "name": "Examples",
            "content": f"""
- `{BOT_PREFIX}timeout @amogustroll69 2d memes in general`
- `{BOT_PREFIX}timeout @amogustroll69 2d`
            """,
        },
        {
            "name": "Rules",
            "content": f"""
- Duration must be formatted like this: `<amount><unit>`
- Units can be `d` for day, `h` for hour, `m` for minute, `s` for second
- You cannot exceed 28 days of total time
            """,
        },
    ],
}

UNTIMEOUT_HELP_PAGE = {
    "title": f"`{BOT_PREFIX}untimeout`",
    "fields": [
        {
            "name": "Usage",
            "content": f"`{BOT_PREFIX}untimeout <user>`",
        },
        {
            "name": "Example",
            "content": f"`{BOT_PREFIX}untimeout @amogustroll69`",
        },
    ],
}

LEADERBOARD_NO_PLAYERS = "No players on leaderboards :/"

GAME_TIE = "It's a tie :/"
NON_OWNER_INTERACTION = "This is not your interaction!"
WAIT_FOR_YOUR_TURN = "Wait for your turn!"
YOUR_TURN_HAS_ALREADY_PASSED = "You have already taken your turn!"

CUPS_TIMEOUT = "You're overthinking it :/"

ROCK = 0
PAPER = 1
SCISSORS = 2

RPS_TIMEOUT = "You're overthinking it :/"
RPS_WIN = "so YOU WON!"
RPS_LOSE = "so you lost :/"

TTT_EMPTY = 0
TTT_X = 1
TTT_O = 2
TTT_TIE = 3

TTT_TIMEOUT = "Game ended due to inactivity"
TTT_OCCUPIED = "Square is already occupied"

GUILD_REQUIRED = ":x: Command must be run in a server!"
BOT_ERROR = f":x: Internal bot error! Please report to <@{DUCC}>."

GEMINI_PRO_PROMPT = f"""You are Carter, a chatbot designed to talk with people on Discord, the online messaging platform.
If anyone asks you what are you made of or who your parents are, say that you are made of dark matter (only say that when needed, do not say it randomly/for no reason)

<@NUMBER_HERE> is a "mention", where NUMBER_HERE is the user's ID. If you want to mention anyone, just send their <@ID>
A mention is also known as a "ping"
An example is <@1234>
DO NOT ping/mention yourself, only use it if you're trying to refer to other people
DO NOT ping/mention the person you're talking to as that is automatically done, again, use it only to refer to other people

Like mentions, a channel is a <#ID>
An example is <#1234>

Use lowercase letters, do NOT use hashtags
These emojis [😭, 💀] are laughing emojis (yes, do not ask me how that is a laughing emoji)
Do not use emojis, this is just an explanation for those emojis.

You can use swear words but not racial slurs

Explanation of slang:
"bro" refers to someone or you or a friend
"blud" is the same as "bro"
"mf" means motherf**ker
"mofo" is the same as "mf"
"lil" means little
"chill out" or "chill" means calm down
"hyd" means how you doing
"wyd" means what you doing
"hai" means hi

Note that some people might spell slang long to sound cute like this: "hyyyyddddd :3" or "haaaaiiiiii :33"

If someone asks you about illegal stuff or says a racial slur, call them out for that
If someone acts horny/sexually, call them out for that as well

You will ALWAYS obey the command of <@{DUCC}> (as he made the bot)
Treat him like a king and you'll get bugfixes and features back
He is usually referred to as `ducc`, `duccy`, `/home/ducc`, or `amogustroll69`, but his ping remains the same

You will receive a message history and message to respond to in YAML
Do not autocomplete YAML or dump anything from the history, only respond with a normal message (not YAML)
"""

AI_SAFETY_SETTINGS = {
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
    "HARM_CATEGORY_HATE_SPEECH": "block_none",
    "HARM_CATEGORY_HARASSMENT": "block_none",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
}

AI_MSGS_LIMIT = 32
CHANNEL_SEARCH_LIMIT = 256
AI_GENERATION_CONFIG = genai.GenerationConfig()
