from discord.ext import commands
from discord import Embed, Color
from games.cups import Cups
from games.rps import RPSGame
import asyncio, tools, constants, logger, db


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = db.DB()

    @commands.command()
    async def leaderboard(self, ctx: commands.Context, game: str | None) -> None:
        await ctx.typing()

        supported_games = [
            "cups",
            "rps",
        ]

        if not game or game not in supported_games:
            await ctx.reply(
                embed=tools.create_embed(
                    "`cb!leaderboard`", constants.LEADERBOARD_HELP_PAGE
                )
            )

            return

        self.db.load()
        leaderboard = self.db.get_leaderboard(game)

        if len(leaderboard) > 0:
            players = ""
            count = 0

            for player in leaderboard:
                players += f"{count + 1}: <@{player}> with {leaderboard[player]} wins\n"

                count += 1

                if count >= 10:
                    break

            embed = Embed(
                title="Leaderboard",
                description=players.strip(),
                color=Color.random(),
            )

            await ctx.send(embed=embed, silent=True)
            return

        await ctx.send(constants.LEADERBOARD_NO_PLAYERS)

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        msg = await ctx.reply(":game_die: Rolling...")
        await asyncio.sleep(2)
        await msg.edit(
            content=f":game_die: The dice landed on {tools.random.randint(1, 6)}!"
        )

    @commands.command()
    async def wyr(self, ctx: commands.Context) -> None:
        await ctx.typing()

        try:
            await ctx.reply(await tools.get_wyr())
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(constants.ERROR)

    @commands.command()
    async def cups(self, ctx: commands.Context) -> None:
        msg = await ctx.reply("Pick the cup:")
        await msg.edit(view=Cups(msg=msg, ctx=ctx, db=self.db))

    @commands.command()
    async def rps(self, ctx: commands.Context) -> None:
        msg = await ctx.reply("Pick one:")
        await msg.edit(view=RPSGame(msg=msg, ctx=ctx, db=self.db))


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
