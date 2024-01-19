from io import BytesIO
from discord.ext import commands
import discord, logger, tools.fun.apis, tools.random, os


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context) -> None:
        cat_bytes = BytesIO()
        cat_ext = ""
        error = ""

        async with ctx.typing():
            try:
                cat_bytes, cat_ext = await tools.fun.apis.get_cat()
            except Exception as e:
                logger.error(str(e))
                error = str(e)

        if error:
            await ctx.reply(f"`{error}`")
            return

        await ctx.reply(file=discord.File(cat_bytes, f"cat{cat_ext}"))

    @commands.command()
    async def dog(self, ctx: commands.Context) -> None:
        dog_bytes = BytesIO()
        dog_ext = ""
        error = ""

        async with ctx.typing():
            try:
                dog_bytes, dog_ext = await tools.fun.apis.get_dog()
            except Exception as e:
                logger.error(str(e))
                error = str(e)

        if error:
            await ctx.reply(f"`{error}`")
            return

        await ctx.reply(file=discord.File(dog_bytes, f"dog{dog_ext}"))

    @commands.command()
    async def fact(self, ctx: commands.Context) -> None:
        fact = ""

        async with ctx.typing():
            try:
                fact = await tools.fun.apis.get_fact()
                fact = fact.replace("`", "\\`")
            except Exception as e:
                logger.error(str(e))
                fact = f"`{e}`"
                return

        await ctx.reply(fact)

    @commands.command()
    async def meme(self, ctx: commands.Context) -> None:
        meme_title = ""
        meme_bytes = BytesIO()
        meme_ext = ""
        error = ""

        meme_nsfw = True

        if type(ctx.channel) is discord.TextChannel and ctx.channel.is_nsfw():
            try:
                (
                    meme_title,
                    meme_bytes,
                    meme_ext,
                    meme_nsfw,
                ) = await tools.fun.apis.get_meme()
            except Exception as e:
                logger.error(str(e))
                error = str(e)

        while meme_nsfw:
            try:
                (
                    meme_title,
                    meme_bytes,
                    meme_ext,
                    meme_nsfw,
                ) = await tools.fun.apis.get_meme()
            except Exception as e:
                logger.error(str(e))
                error = str(e)

            meme_title = meme_title.replace("`", "'")

        if error:
            await ctx.reply(f"`{error}`")
            return

        await ctx.reply(
            content=f"`{meme_title}`:",
            file=discord.File(meme_bytes, f"meme{meme_ext}"),
        )

    @commands.command("a-pussy")
    async def pussy(self, ctx: commands.Context):
        await ctx.reply("https://tenor.com/view/cat-gif-25381727")

    @commands.command()
    async def ascension(self, ctx: commands.Context):
        await ctx.reply(file=discord.File("static/ascension.mp3"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
