from discord.ext import commands
import constants


def ownerOrPerms(**perms):
    original = commands.has_permissions(**perms).predicate

    async def extended_check(ctx):
        if ctx.guild is None:
            return False

        return ctx.author.id == constants.KRILL or await original(ctx)

    return commands.check(extended_check)
