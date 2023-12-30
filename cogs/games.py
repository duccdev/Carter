from discord.ext import commands
from discord import Embed, Color, TextChannel
from games.cups import Cups
from games.rps import RPSGame
import asyncio, tools, constants, db, logger


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
                    f"`{constants.BOT_PREFIX}leaderboard`",
                    constants.LEADERBOARD_HELP_PAGE,
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

            await ctx.send(embed=embed)
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
    async def cups(self, ctx: commands.Context) -> None:
        msg = await ctx.reply("Pick the cup:")
        await msg.edit(view=Cups(msg=msg, ctx=ctx, db=self.db))

    @commands.command()
    async def rps(self, ctx: commands.Context) -> None:
        msg = await ctx.reply("Pick one:")
        await msg.edit(view=RPSGame(msg=msg, ctx=ctx, db=self.db))

    @commands.command()
    async def truth(self, ctx: commands.Context, rating: str | None) -> None:
        await ctx.typing()

        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            embed = tools.create_embed(
                f"`{constants.BOT_PREFIX}truth`",
                constants.TRUTH_HELP_PAGE,
            )
            await ctx.reply(embed=embed)
            return

        if rating == "r" and (
            isinstance(ctx.channel, TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            truth = await tools.get_truth(rating)
            self.db.add_msg(
                f'<@{ctx.author.id}> ({ctx.author.name}): give me a "truth or dare" truth question\nCranberryBot: {truth.lower()[:-1]}'
            )
            await ctx.reply(truth)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def dare(self, ctx: commands.Context, rating: str | None) -> None:
        await ctx.typing()

        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            embed = tools.create_embed(
                f"`{constants.BOT_PREFIX}dare`",
                constants.DARE_HELP_PAGE,
            )
            await ctx.reply(embed=embed)
            return

        if rating == "r" and (
            isinstance(ctx.channel, TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            dare = await tools.get_dare(rating)
            self.db.add_msg(
                f'<@{ctx.author.id}> ({ctx.author.name}): give me a "truth or dare" dare\nCranberryBot: {dare.lower()[:-1]}'
            )
            await ctx.reply(dare)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def wyr(self, ctx: commands.Context, rating: str | None) -> None:
        await ctx.typing()

        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            embed = tools.create_embed(
                f"`{constants.BOT_PREFIX}wyr`",
                constants.WYR_HELP_PAGE,
            )
            await ctx.reply(embed=embed)
            return

        if rating == "r" and (
            isinstance(ctx.channel, TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            wyr = await tools.would_you_rather(rating)
            self.db.add_msg(
                f"<@{ctx.author.id}> ({ctx.author.name}): give me a would you rather question\nCranberryBot: {wyr.lower()[:-1]}"
            )
            await ctx.reply(wyr)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def nhie(self, ctx: commands.Context, rating: str | None) -> None:
        await ctx.typing()

        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            embed = tools.create_embed(
                f"`{constants.BOT_PREFIX}nhie`",
                constants.NHIE_HELP_PAGE,
            )
            await ctx.reply(embed=embed)
            return

        if rating == "r" and (
            isinstance(ctx.channel, TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            nhie = await tools.never_have_i_ever(rating)
            self.db.add_msg(
                f"<@{ctx.author.id}> ({ctx.author.name}): give me a never have i ever question\nCranberryBot: {nhie.lower()[:-1]}"
            )
            await ctx.reply(nhie)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
