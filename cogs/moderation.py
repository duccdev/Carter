from discord.ext import commands
import constants, tools, discord, checks


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @checks.owner_or_perms(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        *reason: str,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.create_embed(constants.BAN_HELP_PAGE))
            return

        if user == self.bot.user:
            await ctx.reply("NEGAWATT")
            return

        if user == ctx.author:
            await ctx.reply("but why tho :skull:")
            return

        if user.id == constants.KRILL:
            await ctx.reply("AIN'T NO WAY :skull_crossbones:")
            return

        if not ctx.guild:
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = "".join([f"{word} " for word in reason])

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.ban_members:
            await ctx.reply(":x: I don't have the permission to ban!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot ban a user higher than me!")
            return

        await user.send(
            f"You have been banned from **{ctx.guild.name}**\nReason: **{reason_str.strip() or 'Unprovided'}**"
        )
        await ctx.guild.ban(user)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.owner_or_perms(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        user: discord.User | None,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.create_embed(constants.UNBAN_HELP_PAGE))
            return

        if not ctx.guild:
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.ban_members:
            await ctx.reply(":x: I don't have the permission to unban!")
            return

        try:
            await ctx.guild.unban(user)
            await ctx.message.add_reaction("✅")
        except discord.NotFound:
            await ctx.reply(":x: User is already unbanned!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
