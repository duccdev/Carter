from discord.ext import commands
from discord import Embed, Color, TextChannel
from emoji import is_emoji
import constants, tools


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = tools.create_embed("Help", constants.HELP_PAGE)

        if self._bot.user:  # i have to do this so python wont annoy me
            embed.set_thumbnail(url=self._bot.user.display_avatar)

        await ctx.send(embed=embed)

    @commands.command()
    # @commands.has_permissions(manage_channels=True)
    async def poll(
        self,
        ctx: commands.Context,
        channel: TextChannel | None,
        poll: str | None,
        *args,
    ) -> None:
        help_page = tools.create_embed("`cb!poll`", constants.POLL_HELP_PAGE)

        if not channel or not poll:
            await ctx.reply(embed=help_page)
            return

        for arg in args:
            if not is_emoji(arg):
                await ctx.reply(embed=help_page)
                return

        embed = Embed(
            title=f"Poll by {ctx.message.author.display_name}",
            description=poll,
            color=Color.random(),
        )

        msg = await channel.send(embed=embed)

        for arg in args:
            await msg.add_reaction(arg)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
