from discord.ext import commands
import discord
import strings
import logger
import tools


class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def nsfw(
        self,
        ctx: commands.Context,
        category: str = "unset",
        content_type: str = "unset",
    ) -> None:
        await ctx.typing()

        if type(ctx.channel) is discord.TextChannel and not ctx.channel.is_nsfw():
            await ctx.send(strings.NSFW_WRONG_CHANNEL)
            return

        if category == "unset":
            await ctx.send(strings.NSFW_USAGE)
            return

        try:
            nsfw_bytes, nsfw_ext = await tools.get_nsfw(category, content_type)
        except tools.NsfwNotFoundError as e:
            await ctx.send(strings.NSFW_NOT_FOUND)
            return
        except Exception as e:
            logger.error(e)
            await ctx.send(strings.ERROR)
            return

        await ctx.send(file=discord.File(nsfw_bytes, f"cat{nsfw_ext}"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NSFW(bot))
