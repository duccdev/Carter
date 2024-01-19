from typing import Literal
from discord.ext import commands
from datetime import datetime, timedelta
import constants, tools.other, tools.db, discord, checks


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def run_checks(
        self, ctx: commands.Context, member: discord.Member | None
    ) -> Literal["SHOW_HELP"] | Literal["INTERNAL_ERROR"] | Literal[
        "HANDLED"
    ] | Literal["SUCCESS"]:
        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)

        if not member:
            return "SHOW_HELP"

        if not ctx.guild or not self.bot.user:
            return "INTERNAL_ERROR"

        if member == self.bot.user or member == ctx.author:
            await ctx.reply(":x: Cannot warn yourself or bot!")
            return "HANDLED"

        member = ctx.guild.get_member(member.id)

        if not member:
            await ctx.reply(":x: User is not a member of this server!")
            return "HANDLED"

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return "INTERNAL_ERROR"

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to view warns!")
            return "HANDLED"

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot view warns of a member higher than me!")
            return "HANDLED"

        return "SUCCESS"

    @commands.command()
    @checks.ownerOrPerms(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        *reason: str,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.WARN_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not member:
            await ctx.reply(embed=tools.other.create_embed(constants.WARN_HELP_PAGE))
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        member = ctx.guild.get_member(member.id)

        if not member:
            await ctx.reply(":x: User is not a member of this server!")
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip()
        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.ban_members:
            await ctx.reply(":x: I don't have the permission to ban!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot ban a member higher than me!")
            return

        await member.send(
            f"You have been banned from **{ctx.guild.name}**\nReason: **{reason_str.strip() or 'Unprovided'}**"
        )
        await ctx.guild.ban(member, reason=reason_str)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        member: None,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.WARN_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not member:
            await ctx.reply(embed=tools.other.create_embed(constants.WARN_HELP_PAGE))
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
            await ctx.guild.unban(member)
            await ctx.message.add_reaction("✅")
        except discord.NotFound:
            await ctx.reply(":x: User is already unbanned!")

    @commands.command()
    @checks.ownerOrPerms(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        *reason: str,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.WARN_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not member:
            await ctx.reply(embed=tools.other.create_embed(constants.WARN_HELP_PAGE))
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        reason_str = ("".join([f"{word} " for word in reason])).strip()
        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to kick!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot kick a member higher than me!")
            return

        await member.send(
            f"You have been kicked from **{ctx.guild.name}**\nReason: **{reason_str.strip() or 'Unprovided'}**"
        )
        await ctx.guild.kick(member, reason=reason_str)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        *reason: str,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.WARN_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not member:
            await ctx.reply(embed=tools.other.create_embed(constants.WARN_HELP_PAGE))
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        reason_str = " ".join([word for word in reason])

        if not reason_str:
            await ctx.reply(embed=tools.other.create_embed(constants.WARN_HELP_PAGE))
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to warn!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot warn a member higher than me!")
            return

        await tools.db.add_warn(ctx.guild, member, reason_str)

        await member.send(
            f"You have been warned in **{ctx.guild.name}**\nReason: **{reason_str}**"
        )

        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def warns(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.WARNS_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not member:
            return

        warns = await tools.db.get_warns(member)

        embed = discord.Embed(
            color=discord.Color.random(),
            title=f"{len(warns)} warn{'s' if len(warns) != 1 else ''}",
        )

        inlines = 0
        for warn in warns:
            if inlines == 2:
                inlines = 0

                embed.add_field(name=f"**{warn.id}**", value=warn.reason, inline=False)
                continue

            inlines += 1
            embed.add_field(
                name=f"**{warn.id}** (**{(warn.expires_at - datetime.now()).days or 1} days** left)",
                value=warn.reason,
                inline=True,
            )

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def unwarn(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        warn_id: str | None,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.UNWARN_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not warn_id or not member:
            await ctx.reply(embed=tools.other.create_embed(constants.UNWARN_HELP_PAGE))
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not bot_member:
            return

        if not bot_member.guild_permissions.moderate_members:
            await ctx.reply(":x: I don't have the permission to unwarn!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot unwarn a member higher than me!")
            return

        try:
            warn_id_int = int(warn_id)
        except:
            await ctx.reply(embed=tools.other.create_embed(constants.WARNS_HELP_PAGE))
            return

        if await tools.db.remove_warn(warn_id_int, member):
            await ctx.message.add_reaction("✅")
            return

        await ctx.reply(":x: Invalid warn ID")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        duration: str | None,
        *reason: str,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.TIMEOUT_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not duration or not member or not bot_member:
            return

        try:
            duration_delta = tools.other.parse_duration(duration)
        except ValueError as e:
            await ctx.reply(f"`{e}`")
            return

        if duration_delta > timedelta(days=28):
            await ctx.reply("Cannot exceed 28 days for timeout!")
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to timeout!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot timeout a member higher than me!")
            return

        if member.is_timed_out():
            await ctx.reply(":x: Cannot timeout a member that's already timed out!")
            return

        reason_str = " ".join([word for word in reason])

        await member.send(
            f"You have been timed out in **{ctx.guild.name}**\nReason: **{reason_str or 'Unprovided'}**"
        )
        await member.timeout(duration_delta, reason=(reason_str or "Unprovided"))
        await ctx.message.add_reaction("✅")

    @commands.command()
    @checks.ownerOrPerms(moderate_members=True)
    async def untimeout(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
    ) -> None:
        match await self.run_checks(ctx, member):
            case "SHOW_HELP":
                await ctx.reply(
                    embed=tools.other.create_embed(constants.TIMEOUT_HELP_PAGE)
                )
                return
            case "INTERNAL_ERROR":
                await ctx.reply(constants.BOT_ERROR)
                return
            case "HANDLED":
                return

        if not ctx.guild:
            await ctx.reply(constants.GUILD_REQUIRED)
            return

        if not self.bot.user:
            return

        bot_member = ctx.guild.get_member(self.bot.user.id)

        if not member or not bot_member:
            return

        if not bot_member.guild_permissions.kick_members:
            await ctx.reply(":x: I don't have the permission to timeout!")
            return

        if member.top_role.position > bot_member.top_role.position:
            await ctx.reply(":x: Cannot timeout a member higher than me!")
            return

        if not member.is_timed_out():
            await ctx.reply(":x: Cannot untimeout a member that's not timed out!")
            return

        await member.edit(timed_out_until=None)
        await ctx.message.add_reaction("✅")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
