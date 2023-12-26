from discord.ext import commands
from games.cup_game import CupGame
import asyncio, tools, constants, logger


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        msg = await ctx.send(":game_die: Rolling...")
        await asyncio.sleep(2)
        await msg.edit(
            content=f":game_die: The dice landed on {tools.random.randint(1, 6)}!"
        )

    @commands.command()
    async def wyr(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            await ctx.send(await tools.get_wyr())
        except Exception as e:
            logger.error(str(e))
            await ctx.send(constants.ERROR)

    @commands.command()
    async def cups(self, ctx: commands.Context) -> None:
        msg = await ctx.send("Pick the cup:")
        await msg.edit(view=CupGame(timeout=3, msg=msg, ctx=ctx))


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
