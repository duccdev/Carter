from typing import Mapping
from discord.ext import commands


class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    def _lazy_paginate(
        self,
        array: list | tuple | set | Mapping,
        count: int = 3,
    ) -> list:
        array = list(array)
        paginated = []

        temp = []
        for item in array:
            if len(temp) == count:
                paginated.append(temp)
                temp = []

            temp.append(item)

        if len(temp) > 0:
            paginated.append(temp)

        return paginated

    @commands.command("dev-load")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, cog_name: str):
        try:
            await self._bot.load_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.send(
                    f"❌ Error occured while loading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.send(f"✅ Loaded the extension: `{cog_name}`")

    @commands.command("dev-unload")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, cog_name: str):
        try:
            await self._bot.unload_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.send(
                    f"❌ Error occured while unloading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.send(f"✅ Unloaded the extension: `{cog_name}`")

    @commands.command("dev-reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog_name: str):
        try:
            await self._bot.reload_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.send(
                    f"❌ Error occured while reloading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.send(f"✅ Reloaded the extension: `{cog_name}`")

    @commands.command("dev-extensions")
    @commands.is_owner()
    async def extensions(self, ctx: commands.Context):
        msg = "Extension list:\n"
        paginated_extlist = self._lazy_paginate(self._bot.extensions)

        for outerlist in paginated_extlist:
            msg_item = "- "
            extcount = 0

            for extension in outerlist:
                extcount += 1
                msg_item += f"`{extension}`"

                if extcount != len(outerlist):
                    msg_item += ", "

            msg += msg_item + "\n"

        await ctx.send(msg)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Developer(bot))
