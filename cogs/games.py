from discord.ext import commands
import time, tools, strings, logger


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        msg = await ctx.send(":game_die: Rolling...")
        time.sleep(2)
        await msg.edit(content=f":game_die: The dice landed on {tools.randint(1, 6)}!")

    @commands.command()
    async def wyr(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            await ctx.send(await tools.get_wyr())
        except Exception as e:
            logger.error(str(e))
            await ctx.send(strings.ERROR)


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
