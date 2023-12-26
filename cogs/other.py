from discord.ext import commands
from discord import Embed, Color
import strings


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = Embed(title="Help", color=Color.random())

        if self._bot.user:  # i have to do this so python wont annoy me
            embed.set_thumbnail(url=self._bot.user.display_avatar)

        for field in strings.HELP_PAGE:
            embed.add_field(name=field["name"], value=field["content"], inline=False)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
