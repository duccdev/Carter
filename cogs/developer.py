from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Mapping
from discord.ext import commands
from config import BOT_PREFIX
from subprocess import run
from db import DB
import tools, traceback, os


class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = DB()

    def lazy_paginate(
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
            await self.bot.load_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.reply(
                    f"error occured while loading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.reply(f"loaded the extension: `{cog_name}`")

    @commands.command("dev-unload")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, cog_name: str):
        try:
            await self.bot.unload_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.reply(
                    f"error occured while unloading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.reply(f"unloaded the extension: `{cog_name}`")

    @commands.command("dev-reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog_name: str):
        try:
            await self.bot.reload_extension(cog_name)
        except Exception as e:
            if isinstance(e, commands.CheckFailure):
                pass
            else:
                await ctx.reply(
                    f"error occured while reloading the extension `{cog_name}`\n"
                    f"`{e.__class__.__name__}: {str(e)}`"
                )

        await ctx.reply(f"reloaded the extension: `{cog_name}`")

    @commands.command("dev-extensions")
    @commands.is_owner()
    async def extensions(self, ctx: commands.Context):
        msg = "Extension list:\n"
        paginated_extlist = self.lazy_paginate(self.bot.extensions)

        for outerlist in paginated_extlist:
            msg_item = "- "
            extcount = 0

            for extension in outerlist:
                extcount += 1
                msg_item += f"`{extension}`"

                if extcount != len(outerlist):
                    msg_item += ", "

            msg += msg_item + "\n"

        await ctx.reply(msg)

    @commands.command("dev-eval")
    @commands.is_owner()
    async def deveval(self, ctx: commands.Context):
        async with ctx.typing():
            code = tools.reverse_replace(
                ctx.message.content.replace(f"{BOT_PREFIX}dev-eval", "", 1).replace(
                    "```py", "", 1
                ),
                "```",
                "",
                1,
            ).strip()

            if not code:
                await ctx.reply(f"usage: `{BOT_PREFIX}dev-eval <py-codeblock>`")
                return

            stringIO = StringIO()
            ret: Any

            try:
                with redirect_stdout(stringIO):
                    ret = eval(code)
            except Exception:
                tb = traceback.format_exc().strip().replace("`", "'")
                await ctx.reply(f"traceback:\n```py\n{tb}\n```")
                return

            ret = str(ret).strip().replace("`", "'")
            stdout = stringIO.getvalue().strip().replace("`", "'")

            msg = ""

            if stdout:
                msg += f"stdout:\n```\n{stdout}\n```"

            msg += f"return:\n```py\n{ret}\n```"

            await ctx.reply(msg)

    @commands.command("dev-exec")
    @commands.is_owner()
    async def devexec(self, ctx: commands.Context):
        async with ctx.typing():
            code = tools.reverse_replace(
                ctx.message.content.replace(f"{BOT_PREFIX}dev-exec", "", 1).replace(
                    "```py", "", 1
                ),
                "```",
                "",
                1,
            ).strip()

            stringIO = StringIO()
            ret: Any

            try:
                with redirect_stdout(stringIO):
                    ret = exec(code)
            except Exception:
                tb = traceback.format_exc().strip().replace("`", "'")
                await ctx.reply(f"traceback:\n```py\n{tb}\n```")
                return

            ret = str(ret).strip().replace("`", "'")
            stdout = stringIO.getvalue().strip().replace("`", "'")

            msg = ""

            if stdout:
                msg += f"stdout:\n```\n{stdout}\n```"

            msg += f"return:\n```py\n{ret}\n```"

            await ctx.reply(msg)

    @commands.command("dev-run-async")
    @commands.is_owner()
    async def devrunasync(self, ctx: commands.Context):
        async with ctx.typing():
            code = tools.reverse_replace(
                ctx.message.content.replace(
                    f"{BOT_PREFIX}dev-run-async", "", 1
                ).replace("```py", "", 1),
                "```",
                "",
                1,
            ).strip()

            if not code:
                await ctx.reply(f"usage: `{BOT_PREFIX}dev-run-async <py-codeblock>`")
                return

            try:
                exec(
                    "async def __ex(ctx: commands.Context, bot: commands.Bot): "
                    + "\n import discord\n from discord.ext import commands\n "
                    + "".join(f"\n {l}" for l in code.split("\n"))
                )
            except Exception:
                tb = traceback.format_exc().strip().replace("`", "'")
                await ctx.reply(f"traceback:\n```py\n{tb}\n```")
                return

            stringIO = StringIO()
            ret: Any

            try:
                with redirect_stdout(stringIO):
                    ret = await locals()["__ex"](ctx, self.bot)
            except Exception:
                tb = traceback.format_exc().strip().replace("`", "'")
                await ctx.reply(f"traceback:\n```py\n{tb}\n```")
                return

            ret = str(ret).strip().replace("`", "'")
            stdout = stringIO.getvalue().strip().replace("`", "'")

            msg = ""

            if stdout:
                msg += f"stdout:\n```\n{stdout}\n```"

            msg += f"return:\n```py\n{ret}\n```"

            await ctx.reply(msg)

    @commands.command("dev-update")
    @commands.is_owner()
    async def devupdate(self, ctx: commands.Context):
        await ctx.send("running `git pull origin main`...")

        if os.system("git pull origin main") != 0:
            await ctx.send("failed!")
            return

        await ctx.send("updating pip packages...")

        if os.system("pip install -U -r requirements.txt") != 0:
            await ctx.send("failed!")
            return

        await ctx.send("restarting...")
        os.system("sudo systemctl restart CranberryBot")

    @commands.command("dev-system")
    @commands.is_owner()
    async def devsystem(self, ctx: commands.Context, *args):
        async with ctx.typing():
            if len(args) == 0:
                await ctx.reply(f"usage: `{BOT_PREFIX}dev-system <args>`")

            msg = ""
            output = run(args, capture_output=True, text=True)

            if output.stdout:
                msg += f"stdout:\n```\n{output.stdout}\n```\n"

            if output.stderr:
                msg += f"stderr:\n```\n{output.stderr}\n```\n"

            msg += f"return value: `{output.returncode}`"

            await ctx.reply(msg)

    @commands.command("dev-ai-reset")
    @commands.is_owner()
    async def devaireset(self, ctx: commands.Context):
        await ctx.typing()
        self.db.load()
        self.db.clear_msg_history()
        self.db.save()
        await ctx.reply("done")

    @commands.command("dev-update-memes")
    @commands.is_owner()
    async def devupdatememes(self, ctx: commands.Context):
        error = False

        async with ctx.typing():
            if os.system('bash -c "cd krill-memes && git pull origin main"') != 0:
                error = True

        await ctx.reply("failed" if error else "done")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Developer(bot))
