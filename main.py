from discord.ext import commands
from discord import Intents
import logger
import config
import cogs


async def setup_hook() -> None:
    logger.info("Adding cogs...")
    await cranberry.add_cog(cogs.Other(cranberry))
    await cranberry.add_cog(cogs.Fun(cranberry))
    await cranberry.add_cog(cogs.NSFW(cranberry))


cranberry = commands.Bot(config.BOT_PREFIX, intents=Intents.all(), help_command=None)
cranberry.setup_hook = setup_hook


@cranberry.event
async def on_ready() -> None:
    logger.info("Ready!")


cranberry.run(config.TOKEN, log_handler=None)
