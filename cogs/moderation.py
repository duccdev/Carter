from discord.ext import commands
from db import DB
import constants, tools, discord, checks, time, datetime


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = DB()

    @commands.command()
    @checks.ownerOrPerms(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        *reason: str,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.BAN_HELP_PAGE))
            return

        if not ctx.guild:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user or not self.bot.user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip()
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
        await ctx.guild.ban(user, reason=reason_str)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        user: discord.User | None,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.UNBAN_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
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

    @commands.command()
    @checks.ownerOrPerms(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        *reason: str,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.WARN_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip()
        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to kick!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot kick a user higher than me!")
            return

        await user.send(
            f"You have been kicked from **{ctx.guild.name}**\nReason: **{reason_str.strip() or 'Unprovided'}**"
        )
        await ctx.guild.kick(user, reason=reason_str)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def warn(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        *reason: str,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.WARN_HELP_PAGE))
            return

        if not ctx.guild:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user or not self.bot.user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip()

        if not reason_str:
            await ctx.reply(embed=tools.createEmbed(constants.WARN_HELP_PAGE))
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to warn!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot warn a user higher than me!")
            return

        warn_id = self.db.addWarn(user.id, reason_str)
        warns = len(self.db.getWarns(user.id))

        await user.send(
            f"You have been warned in **{ctx.guild.name}**\nReason: **{reason_str}**"
        )

        embed = discord.Embed(color=discord.Color.random(), title="Warn")

        embed.add_field(name="ID", value=warn_id, inline=False)
        embed.add_field(name="Reason", value=reason_str, inline=False)
        embed.add_field(name="Expires in", value="**30 days**", inline=False)
        embed.add_field(name="All warns", value=str(warns), inline=False)

        await ctx.reply(embed=embed)

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def warns(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.WARNS_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to view warns!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot view warns of a user higher than me!")
            return

        warns = self.db.getWarns(user.id)

        embed = discord.Embed(color=discord.Color.random(), title=f"{len(warns)} warns")

        for key in warns:
            embed.add_field(name="ID", value=key)
            embed.add_field(name="Reason", value=warns[key]["reason"])
            embed.add_field(
                name="Expires in",
                value=f"**{int((warns[key]['expires_in'] - time.time()) // 86400)} days**",
            )

        await ctx.reply(embed=embed)

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def unwarn(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        warn_id: str | None,
    ) -> None:
        if not user or not warn_id:
            await ctx.reply(embed=tools.createEmbed(constants.UNWARN_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to unwarn!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot unwarn a user higher than me!")
            return

        if self.db.remove_warn(user.id, warn_id):
            await ctx.message.add_reaction("✅")
            return

        await ctx.reply(":x: Invalid warn ID")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
        duration: str | None,
        *reason: str,
    ) -> None:
        if not user or not duration:
            await ctx.reply(embed=tools.createEmbed(constants.TIMEOUT_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip() or "Unprovided"
        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        try:
            duration_delta = tools.parseDuration(duration)
        except ValueError as e:
            await ctx.reply(f"`{e}`")
            return

        if duration_delta > datetime.timedelta(days=28):
            await ctx.reply("Cannot exceed 28 days for timeout!")
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to timeout!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot timeout a user higher than me!")
            return

        if user.is_timed_out():
            await ctx.reply(":x: Cannot timeout a user that's already timed out!")
            return

        await user.send(
            f"You have been timed out in **{ctx.guild.name}**\nReason: **{reason_str}**"
        )
        await user.timeout(duration_delta, reason=reason_str)
        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def untimeout(
        self,
        ctx: commands.Context,
        user: discord.User | discord.Member | None,
    ) -> None:
        if not user:
            await ctx.reply(embed=tools.createEmbed(constants.UNTIMEOUT_HELP_PAGE))
            return

        if not ctx.guild or not self.bot.user:
            return

        if user == self.bot.user or user == ctx.author or user.id == constants.KRILL:
            await ctx.reply("NEGAWATT")
            return

        user = ctx.guild.get_member(user.id)

        if not user:
            await ctx.reply(":x: User is not a member of this server!")
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to timeout!")
            return

        if user.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot timeout a user higher than me!")
            return

        if not user.is_timed_out():
            await ctx.reply(":x: Cannot untimeout a user that's not timed out!")
            return

        await user.edit(timed_out_until=None)
        await ctx.message.add_reaction("✅")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
