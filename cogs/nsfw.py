from discord.ext import commands
import discord
import constants
import logger
import tools


class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def nsfw(
        self,
        ctx: commands.Context,
        category: str = "unset",
        content_type: str = "unset",
    ) -> None:
        async with ctx.typing():
            if type(ctx.channel) is discord.TextChannel and not ctx.channel.is_nsfw():
                await ctx.send(constants.NSFW_WRONG_CHANNEL)
                return

            if category == "unset" or content_type == "unset":
                embed = discord.Embed(title="`cb!nsfw`", color=discord.Color.random())

                if self.bot.user:  # i have to do this so python wont annoy me
                    embed.set_thumbnail(url=self.bot.user.display_avatar)

                for field in constants.NSFW_HELP_PAGE:
                    embed.add_field(
                        name=field["name"], value=field["content"], inline=False
                    )

                await ctx.send(embed=embed)

                return

            try:
                nsfw_bytes, nsfw_ext = await tools.get_nsfw(category, content_type)
            except tools.NsfwNotFoundError as e:
                await ctx.send(constants.NSFW_NOT_FOUND)
                return
            except Exception as e:
                logger.error(e)
                await ctx.send(constants.ERROR)
                return

            await ctx.send(file=discord.File(nsfw_bytes, f"cat{nsfw_ext}"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NSFW(bot))
