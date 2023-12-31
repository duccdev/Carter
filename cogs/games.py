from discord.ext import commands
from games.cups import Cups
from games.rps import RPSGame
from games.rpspvp import RPSPVPGame
import asyncio, tools, constants, db, logger, discord


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = db.DB()

    @commands.command()
    async def leaderboard(self, ctx: commands.Context, game: str | None) -> None:
        supported_games = ["cups", "rps", "rps-pvp"]

        if not game or game not in supported_games:
            await ctx.reply(embed=tools.create_embed(constants.LEADERBOARD_HELP_PAGE))
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

            embed = discord.Embed(
                title="Leaderboard",
                description=players.strip(),
                color=discord.Color.random(),
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
        await msg.edit(view=Cups(msg=msg, ctx=ctx))

    @commands.command()
    async def rps(self, ctx: commands.Context) -> None:
        msg = await ctx.reply("Pick one:")
        await msg.edit(view=RPSGame(msg=msg, ctx=ctx))

    @commands.command("rps-pvp")
    async def rpspvp(
        self, ctx: commands.Context, p2: discord.Member | discord.User | None
    ) -> None:
        if not p2:
            await ctx.reply(f"Usage: `{constants.BOT_PREFIX}rps-pvp <other_member>`")
            return

        if p2 == ctx.author:
            await ctx.reply(f"mf just play using {constants.BOT_PREFIX}rps then")
            return

        if p2 == self.bot.user:
            msg = await ctx.reply("Pick one:")
            await msg.edit(view=RPSGame(msg=msg, ctx=ctx))
            return

        msg = await ctx.reply(f"<@{ctx.author.id}> goes first")
        await msg.edit(view=RPSPVPGame(msg=msg, p1_id=ctx.author.id, p2_id=p2.id))

    @commands.command()
    async def truth(self, ctx: commands.Context, rating: str | None) -> None:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            await ctx.reply(embed=tools.create_embed(constants.TRUTH_HELP_PAGE))
            return

        if rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            truth = await tools.get_truth(rating)
            self.db.add_msg(
                ctx.author.id,
                ctx.author.name,
                'give me a "truth or dare" truth question',
                truth.lower()[:-1],
                [],
            )
            await ctx.reply(truth)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def dare(self, ctx: commands.Context, rating: str | None) -> None:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            await ctx.reply(embed=tools.create_embed(constants.DARE_HELP_PAGE))
            return

        if rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            dare = await tools.get_dare(rating)
            self.db.add_msg(
                ctx.author.id,
                ctx.author.name,
                'give me a "truth or dare" dare',
                dare.lower()[:-1],
                [],
            )
            await ctx.reply(dare)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def wyr(self, ctx: commands.Context, rating: str | None) -> None:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            await ctx.reply(embed=tools.create_embed(constants.WYR_HELP_PAGE))
            return

        if rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            wyr = await tools.would_you_rather(rating)
            self.db.add_msg(
                ctx.author.id,
                ctx.author.name,
                "give me a would you rather question",
                wyr.lower()[:-1],
                [],
            )
            await ctx.reply(wyr)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")

    @commands.command()
    async def nhie(self, ctx: commands.Context, rating: str | None) -> None:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating != "pg" and rating != "pg13" and rating != "r":
            await ctx.reply(embed=tools.create_embed(constants.NHIE_HELP_PAGE))
            return

        if rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            nhie = await tools.never_have_i_ever(rating)
            self.db.add_msg(
                ctx.author.id,
                ctx.author.name,
                "give me a never have i ever question",
                nhie.lower()[:-1],
                [],
            )
            await ctx.reply(nhie)
        except Exception as e:
            logger.error(str(e))
            await ctx.reply(f"`{e}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
