import datetime, discord
from prisma import Prisma
from prisma.models import Vote

db = Prisma()


async def db_connect():
    if not db.is_connected():
        await db.connect()


async def get_guild(guild: discord.Guild):
    await db_connect()

    return (await db.guild.find_unique(where={"id": guild.id})) or (
        await db.guild.create(data={"id": guild.id})
    )


async def add_warn(guild: discord.Guild, member: discord.Member, reason: str):
    await db_connect()

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
    await db_connect()

    for warn in await db.warn.find_many():
        if datetime.datetime.utcnow() >= warn.expires_at:
            await db.warn.delete(
                where={
                    "id": warn.id,
                }
            )


async def remove_warn(id: str) -> bool:
    await db_connect()

    warn = await db.warn.find_unique(where={"id": id})

    if not warn:
        return False

    await db.warn.delete(where={"id": id})

    return True


async def get_warns(member: discord.Member):
    await db_connect()

    return await db.warn.find_many(where={"member_id": member.id})


async def get_leaderboard(guild: discord.Guild, name: str):
    await db_connect()
    await get_guild(guild)

    return (await db.leaderboard.find_unique(where={"guild_id": guild.id})) or (
        await db.leaderboard.create(data={"guild_id": guild.id, "name": name})
    )


async def add_win(
    leaderboard: str,
    guild: discord.Guild | None,
    member: discord.User | discord.Member,
):
    await db_connect()

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


async def create_poll():
    await db_connect()

    return await db.poll.create(data={})


async def get_poll(id: str):
    await db_connect()

    return await db.poll.find_unique_or_raise(where={"id": id})


async def set_vote(poll_id: str, member: discord.User | discord.Member, option: int):
    await db_connect()

    poll = await get_poll(poll_id)

    await db.vote.create(
        {
            "poll_id": poll.id,
            "user_id": member.id,
            "option": option,
        }
    )


async def remove_vote(poll_id: str):
    await db_connect()

    await db.vote.delete(where={"poll_id": poll_id})
