from discord.ext import commands
from discord import Intents, Game
from os import getenv
from dotenv import load_dotenv
import logger, config, logging

load_dotenv()

if (
    not getenv("TOKEN")
    or not getenv("CAT_API")
    or not getenv("DOG_API")
    or not getenv("GENAI")
    or not getenv("PGSQL")
    or not getenv("CARTER_ENV")
):
    logger.error("Invalid .env, please consult .env.example and the readme")
    exit(1)

devmode = True if getenv("CARTER_ENV", "prod") == "dev" else False

if devmode:
    logger.info("Running in development mode")

carter = commands.Bot(config.BOT_PREFIX, intents=Intents.all(), help_command=None)


async def setup_hook() -> None:
    logger.info("Adding cogs...")
    await carter.load_extension("cogs.other")
    await carter.load_extension("cogs.fun")
    await carter.load_extension("cogs.games")
    await carter.load_extension("cogs.developer")
    await carter.load_extension("cogs.moderation")


carter.setup_hook = setup_hook


@carter.event
async def on_ready() -> None:
    if devmode:
        await carter.change_presence(activity=Game("with myself (Devmode)"))
    else:
        await carter.change_presence(activity=Game("with myself"))

    logger.info("Ready!")


if devmode:
    carter.run(
        getenv("TOKEN", ""),
        log_handler=logger.LoggingHandler(level=logging.DEBUG),
    )
else:
    carter.run(getenv("TOKEN", ""), log_handler=None)
