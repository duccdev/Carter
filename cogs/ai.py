from discord.ext import commands
import tools.other, tools.ai, config, discord, traceback


class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command("ai-reset")
    async def reset(self, ctx: commands.Context) -> None:
        await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command("ai-count")
    async def count(self, ctx: commands.Context) -> None:
        if not self.bot.user or ctx.message.author == self.bot.user:
            return

        async with ctx.typing():
            try:
                length, tokens = await tools.ai.count(ctx.message, self.bot.user)

                msg = f"Chars: {length}\nTokens: {tokens}"
            except:
                msg = f"```py\n{traceback.format_exc()}```" ""

        await ctx.reply(msg)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        if (
            not self.bot.user
            or msg.author == self.bot.user
            or msg.is_system()
            or msg.author.bot
            or msg.content.startswith(config.BOT_PREFIX)
        ):
            return

        if self.bot.user in msg.mentions or isinstance(msg.channel, discord.DMChannel):
            async with msg.channel.typing():
                content = await tools.ai.send(msg, self.bot.user)

            await msg.reply(content)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
