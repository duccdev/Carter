from discord.ext import commands
import strings


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        await ctx.send(strings.HELP_PAGE, silent=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
