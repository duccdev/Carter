import datetime, discord
from prisma import Prisma

db = Prisma()


async def get_guild(guild: discord.Guild):
    return (await db.guild.find_unique(where={"id": guild.id})) or (
        await db.guild.create(data={"id": guild.id})
    )


async def add_warn(guild: discord.Guild, member: discord.Member, reason: str):
    db_guild = await get_guild(guild)

    await db.warn.create(
        data={
            "guild_id": db_guild.id,
            "member_id": member.id,
            "reason": reason,
            "expires_at": datetime.datetime.utcnow(),
        }
    )


async def expire_warns():
    for warn in await db.warn.find_many():
        if datetime.datetime.utcnow() >= warn.expires_at:
            await db.warn.delete(
                where={
                    "id": warn.id,
                }
            )


async def remove_warn(id: int, member: discord.Member) -> bool:
    warn = await db.warn.find_unique(where={"id": id, "member_id": member.id})

    if not warn:
        return False

    await db.warn.delete(where={"id": id, "member_id": member.id})

    return True


async def get_warns(member: discord.Member):
    return await db.warn.find_many(where={"member_id": member.id})


async def get_leaderboard(guild: discord.Guild, name: str):
    return (
        await db.leaderboard.find_unique(where={"guild_id": guild.id, "name": name})
    ) or (await db.leaderboard.create(data={"guild_id": guild.id, "name": name}))


async def add_win(
    leaderboard: str,
    guild: discord.Guild | None,
    member: discord.User | discord.Member,
):
    if not guild or isinstance(member, discord.User):
        return

    db_leaderboard = await get_leaderboard(guild, leaderboard)
    players = db_leaderboard.players or []

    for player in players:
        if player.id == member.id:
            player.wins += 1
            await db.player.update(
                data={"wins": player.wins},
                where={"leaderboard_id": db_leaderboard.id},
            )
            return

    await db.player.create(
        data={
            "id": member.id,
            "leaderboard_id": db_leaderboard.id,
            "wins": 1,
        },
    )
