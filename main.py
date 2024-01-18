from discord.ext import commands
from discord import Intents, Game
import logger, config, logging


devmode = True if config.CARTER_ENV == "dev" else False

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
    carter.run(config.TOKEN, log_handler=logger.LoggingHandler(level=logging.DEBUG))
else:
    carter.run(config.TOKEN, log_handler=None)
