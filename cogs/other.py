from discord.ext import commands
from views.help import HelpView
import constants, tools.other, checks, discord


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, page: str | None) -> None:
        if page and page in constants.HELP_PAGES:
            embed = tools.other.create_embed(constants.HELP_PAGES[page])
        else:
            embed = tools.other.create_embed(constants.HELP_PAGES["main"])

        await ctx.reply(embed=embed, view=HelpView(sender=ctx.author.id))

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.reply(f":ping_pong: `{self.bot.latency}`")

    @commands.command()
    async def contributors(self, ctx: commands.Context):
        await ctx.reply(embed=tools.other.create_embed(constants.CONTRIBUTORS))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
