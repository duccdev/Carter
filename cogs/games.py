import traceback
from discord.ext import commands
from games.cups import Cups
from games.rps import RPSGame
from games.rpspvp import RPSPVPGame
from games.tictactoe import TicTacToe
import asyncio, tools.other, tools.random, tools.games.truth_or_dare, tools.games.never_have_i_ever, tools.games.would_you_rather, tools.db, constants, logger, discord


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def check_rating(self, ctx: commands.Context, rating: str | None) -> str:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating not in ["pg", "pg13", "r"]:
            return "HELP_PAGE"
        elif rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return "HANDLED"

        return rating

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context, game: str | None) -> None:
        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        supported_games = ["cups", "rps", "rps-pvp", "tictactoe"]

        if not game or game not in supported_games:
            await ctx.reply(
                embed=tools.other.create_embed(constants.LEADERBOARD_HELP_PAGE)
            )
            return

        leaderboard = (await tools.db.get_leaderboard(ctx.guild, game)).players or []

        if len(leaderboard) > 0:
            players = ""
            count = 0

            for player in leaderboard:
                players += f"{count + 1}: <@{player.id}> with {player.wins} wins\n"

                count += 1

                if count >= 10:
                    break

            embed = discord.Embed(
                title="Leaderboard",
                description=players.strip(),
                color=discord.Color.random(),
            )

            await ctx.reply(embed=embed)
            return

        await ctx.reply(constants.LEADERBOARD_NO_PLAYERS)

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
        self,
        ctx: commands.Context,
        p2: discord.Member | discord.User | None,
    ) -> None:
        if not p2:
            await ctx.reply(f"Usage: `{constants.BOT_PREFIX}rps-pvp <other_member>`")
            return

        if p2 == ctx.author:
            await ctx.reply(f"You can't PvP yourself!")
            return

        if p2 == self.bot.user:
            msg = await ctx.reply("Pick one:")
            await msg.edit(view=RPSGame(msg=msg, ctx=ctx))
            return

        if not isinstance(p2, discord.Member) or not isinstance(
            ctx.author, discord.Member
        ):
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        msg = await ctx.reply(f"<@{ctx.author.id}> goes first")
        await msg.edit(view=RPSPVPGame(msg=msg, p1=ctx.author, p2=p2))

    @commands.command()
    async def tictactoe(
        self,
        ctx: commands.Context,
        opponent: discord.Member | discord.User | None,
    ) -> None:
        if not opponent:
            await ctx.reply(f"Usage: `{constants.BOT_PREFIX}tictactoe <other_member>`")
            return

        if opponent == ctx.author or opponent == self.bot.user:
            await ctx.reply(f"You can't PvP me or yourself!")
            return

        if not isinstance(opponent, discord.Member) or not isinstance(
            ctx.author, discord.Member
        ):
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        await ctx.reply(
            f"It's <@{ctx.author.id}>'s turn",
            view=TicTacToe(player_x=ctx.author, player_o=opponent),
        )

    @commands.command()
    async def truth(self, ctx: commands.Context, rating: str | None) -> None:
        if not rating:
            rating = tools.random.choice(["pg", "pg13"])
        elif rating not in ["pg", "pg13", "r"]:
            await ctx.reply(embed=tools.other.create_embed(constants.TRUTH_HELP_PAGE))
            return

        if rating == "r" and (
            isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.is_nsfw()
        ):
            await ctx.reply("ayo?! (hint: use R rating in an NSFW channel)")
            return

        try:
            await ctx.reply(await tools.games.truth_or_dare.get_truth(rating))
        except:
            logger.error(traceback.format_exc())
            await ctx.reply(
                f":x: Internal bot error! Please report to <@{constants.KRILL}>."
            )

    @commands.command()
    async def dare(self, ctx: commands.Context, rating: str | None) -> None:
        rating = await self.check_rating(ctx, rating)

        if rating == "HANDLED":
            return

        if rating == "HELP_PAGE":
            await ctx.reply(embed=tools.other.create_embed(constants.DARE_HELP_PAGE))
            return

        try:
            await ctx.reply(await tools.games.truth_or_dare.get_dare(rating))
        except:
            logger.error(traceback.format_exc())
            await ctx.reply(
                f":x: Internal bot error! Please report to <@{constants.KRILL}>."
            )

    @commands.command()
    async def wyr(self, ctx: commands.Context, rating: str | None) -> None:
        rating = await self.check_rating(ctx, rating)

        if rating == "HANDLED":
            return

        if rating == "HELP_PAGE":
            await ctx.reply(embed=tools.other.create_embed(constants.WYR_HELP_PAGE))
            return

        try:
            await ctx.reply(await tools.games.would_you_rather.get_wyr(rating))
        except:
            logger.error(traceback.format_exc())
            await ctx.reply(
                f":x: Internal bot error! Please report to <@{constants.KRILL}>."
            )

    @commands.command()
    async def nhie(self, ctx: commands.Context, rating: str | None) -> None:
        rating = await self.check_rating(ctx, rating)

        if rating == "HANDLED":
            return

        if rating == "HELP_PAGE":
            await ctx.reply(embed=tools.other.create_embed(constants.NHIE_HELP_PAGE))
            return

        try:
            await ctx.reply(await tools.games.never_have_i_ever.get_nhie(rating))
        except:
            logger.error(traceback.format_exc())
            await ctx.reply(
                f":x: Internal bot error! Please report to <@{constants.KRILL}>."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
