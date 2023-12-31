from io import BytesIO
from discord.ext import commands
import discord, logger, constants, tools, os


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context) -> None:
        cat_bytes = BytesIO()
        cat_ext = ""
        error = False

        async with ctx.typing():
            try:
                cat_bytes, cat_ext = await tools.get_cat()
            except Exception as e:
                logger.error(e)
                error = True
                return

        await ctx.typing()

        if error:
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(file=discord.File(cat_bytes, f"dog{cat_ext}"))

    @commands.command()
    async def dog(self, ctx: commands.Context) -> None:
        dog_bytes = BytesIO()
        dog_ext = ""
        error = False

        async with ctx.typing():
            try:
                dog_bytes, dog_ext = await tools.get_dog()
            except Exception as e:
                logger.error(e)
                error = True
                return

        await ctx.typing()

        if error:
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(file=discord.File(dog_bytes, f"dog{dog_ext}"))

    @commands.command()
    async def fact(self, ctx: commands.Context) -> None:
        fact = ""

        async with ctx.typing():
            try:
                fact = await tools.get_fact()
                fact = fact.replace("`", "\\`")
            except Exception as e:
                logger.error(e)
                fact = constants.ERROR
                return

        await ctx.typing()

        await ctx.reply(fact)

    @commands.command()
    async def meme(self, ctx: commands.Context) -> None:
        meme_title = ""
        meme_bytes = BytesIO()
        meme_ext = ""
        error = False

        async with ctx.typing():
            meme_nsfw = True

            if type(ctx.channel) is discord.TextChannel and ctx.channel.is_nsfw():
                try:
                    meme_title, meme_bytes, meme_ext, meme_nsfw = await tools.get_meme()
                except Exception as e:
                    logger.error(e)
                    error = True
                    return

            while meme_nsfw:
                try:
                    meme_title, meme_bytes, meme_ext, meme_nsfw = await tools.get_meme()
                except Exception as e:
                    logger.error(e)
                    error = True
                    return

            meme_title = meme_title.replace("`", "'")

        await ctx.typing()

        if error:
            await ctx.reply(constants.ERROR)
            return

        await ctx.reply(
            content=f"`{meme_title}`:",
            file=discord.File(meme_bytes, f"meme{meme_ext}"),
        )

    @commands.command("krill-meme")
    async def krillmeme(self, ctx: commands.Context):
        await ctx.typing()

        memes = os.listdir("krill-memes")

        try:
            memes.remove(".git")
        except:
            pass

        try:
            memes.remove(".gitignore")
        except:
            pass

        if not memes:
            await ctx.reply(
                "the fucker <@719562834295390299> forgot to update my krill memes collection"
            )
            return

        await ctx.reply(file=discord.File(f"krill-memes/{tools.random.choice(memes)}"))

    @commands.command("a-pussy")
    async def pussy(self, ctx: commands.Context):
        await ctx.typing()
        await ctx.reply("https://tenor.com/view/cat-gif-25381727")

    @commands.command()
    async def ascension(self, ctx: commands.Context):
        await ctx.typing()
        await ctx.reply(file=discord.File("static/ascension.mp3"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
