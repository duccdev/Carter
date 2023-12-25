from discord.ext import commands
import time, secrets

randint = lambda min, max: secrets.randbelow(max) + min


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot = bot

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        msg = await ctx.send(":game_die: Rolling...")
        time.sleep(2)
        await msg.edit(content=f":game_die: The dice landed on {randint(1, 6)}!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
