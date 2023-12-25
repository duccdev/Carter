from discord.ext import commands
from discord import Intents, Game
from os import getenv
import logger
import config

devmode = True if getenv("CRANBERRY_ENV", "prod") == "dev" else False

if devmode:
    logger.info("Running in development mode")


async def setup_hook() -> None:
    logger.info("Adding cogs...")
    await cranberry.load_extension("cogs.other")
    await cranberry.load_extension("cogs.fun")
    await cranberry.load_extension("cogs.nsfw")


cranberry = commands.Bot(config.BOT_PREFIX, intents=Intents.all(), help_command=None)
cranberry.setup_hook = setup_hook


@cranberry.event
async def on_ready() -> None:
    if devmode:
        await cranberry.change_presence(activity=Game("with myself (Development)"))

    logger.info("Ready!")


if devmode:
    cranberry.run(config.TOKEN)
else:
    cranberry.run(config.TOKEN, log_handler=None)
