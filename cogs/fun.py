from io import BytesIO
from discord.ext import commands
import discord
import logger
import constants
import tools


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            cat_bytes, cat_ext = await tools.get_cat()
        except Exception as e:
            logger.error(e)
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(file=discord.File(cat_bytes, f"cat{cat_ext}"))

    @commands.command()
    async def dog(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            dog_bytes, dog_ext = await tools.get_dog()
        except Exception as e:
            logger.error(e)
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(file=discord.File(dog_bytes, f"dog{dog_ext}"))

    @commands.command()
    async def fact(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            fact = await tools.get_fact()
            fact = fact.replace("`", "\\`")
        except Exception as e:
            logger.error(e)
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(fact)

    @commands.command()
    async def meme(self, ctx: commands.Context) -> None:
        await ctx.typing()

        meme_title = ""
        meme_bytes = BytesIO()
        meme_ext = ""
        meme_nsfw = True

        if type(ctx.channel) is discord.TextChannel and ctx.channel.is_nsfw():
            try:
                meme_title, meme_bytes, meme_ext, meme_nsfw = await tools.get_meme()
            except Exception as e:
                logger.error(e)
                await ctx.reply(constants.ERROR)
                return

        while meme_nsfw:
            try:
                meme_title, meme_bytes, meme_ext, meme_nsfw = await tools.get_meme()
            except Exception as e:
                logger.error(e)
                await ctx.reply(constants.ERROR)
                return

        meme_title = meme_title.replace("`", "'")
        await ctx.reply(
            content=f"`{meme_title}`:", file=discord.File(meme_bytes, f"meme{meme_ext}")
        )

    @commands.command("a-pussy")
    async def pussy(self, ctx: commands.Context):
        await ctx.typing()
        await ctx.reply(file=discord.File("static/a-pussy.gif"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
