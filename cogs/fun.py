from io import BytesIO
from discord.ext import commands
import discord
import logger
import strings
import tools
import time
import random


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            cat_bytes, cat_ext = await tools.get_cat()
        except Exception as e:
            logger.error(e)
            await ctx.send(strings.ERROR)
            return

        await ctx.send(file=discord.File(cat_bytes, f"cat{cat_ext}"))

    @commands.command()
    async def dog(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            dog_bytes, dog_ext = await tools.get_dog()
        except Exception as e:
            logger.error(e)
            await ctx.send(strings.ERROR)
            return

        await ctx.send(file=discord.File(dog_bytes, f"dog{dog_ext}"))

    @commands.command()
    async def fact(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            fact = await tools.get_fact()
            fact = fact.replace("`", "\\`")
        except Exception as e:
            logger.error(e)
            await ctx.send(strings.ERROR)
            return

        await ctx.send(fact)

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        msg = await ctx.send(":game_die: Rolling...")
        time.sleep(2)
        await msg.edit(content=f":game_die: The dice landed on {random.randint(1, 6)}!")

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
                await ctx.send(strings.ERROR)
                return

        while meme_nsfw:
            try:
                meme_title, meme_bytes, meme_ext, meme_nsfw = await tools.get_meme()
            except Exception as e:
                logger.error(e)
                await ctx.send(strings.ERROR)
                return

        meme_title = meme_title.replace("`", "'")
        await ctx.send(
            content=f"`{meme_title}`:", file=discord.File(meme_bytes, f"meme{meme_ext}")
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
