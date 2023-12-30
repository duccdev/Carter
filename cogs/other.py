from discord.ext import commands
from discord import TextChannel, Embed, Message, Color
from db import DB
from views.poll import Poll
import constants, tools, PIL.Image, os, ai, logger, checks


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = DB()

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = tools.create_embed("Help", constants.HELP_PAGE)

        if self.bot.user:  # i have to do this so python wont annoy me
            embed.set_thumbnail(url=self.bot.user.display_avatar)

        await ctx.reply(embed=embed)

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.typing()
        await ctx.reply(f":ping_pong: `{tools.ping()}`")

    @commands.command()
    @checks.owner_or_perms(
        manage_channels=True,
        manage_messages=True,
        send_messages=True,
    )
    async def poll(
        self,
        ctx: commands.Context,
        channel: TextChannel | None,
        poll: str | None,
        options: str | None,
    ) -> None:
        help_page = tools.create_embed(
            f"`{constants.BOT_PREFIX}poll`", constants.POLL_HELP_PAGE
        )

        if not channel or not poll or not options:
            await ctx.reply(embed=help_page)
            return

        try:
            options_int = int(options)
        except:
            await ctx.reply(embed=help_page)
            return

        if options_int > 10 or options_int < 1:
            await ctx.reply(embed=help_page)
            return

        embed = Embed(
            title=f"Poll by {ctx.message.author.display_name}",
            description=poll,
            color=Color.random(),
        )

        await channel.send(
            embed=embed,
            view=Poll(options=list(range(1, options_int + 1))),
        )

    @commands.command("ai-reset")
    async def aireset(self, ctx: commands.Context):
        await ctx.typing()
        history = self.db.get_msg_history().splitlines()
        new_history = history

        for line in history:
            if str(ctx.author.id) in line:
                new_history.remove(line)

        self.db.set_msg_history("".join(new_history))
        await ctx.reply("Done! :thumbsup:")

    @commands.command()
    async def contributors(self, ctx: commands.Context):
        await ctx.reply(
            embed=tools.create_embed("Contributors", constants.CONTRIBUTORS)
        )

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        if not self.bot.user:
            return

        if msg.author.id == self.bot.user.id:
            return

        if self.bot.user in msg.mentions:
            async with msg.channel.typing():
                imgs: list[PIL.Image.Image] = []

                if msg.attachments:
                    for attachment in msg.attachments:
                        if (
                            attachment.content_type
                            and attachment.content_type.startswith("image/")
                            and attachment.content_type != "image/gif"
                        ):
                            imgpath = f"/tmp/{attachment.filename}"

                            with open(imgpath, "wb") as fp:
                                await attachment.save(fp)

                            img = PIL.Image.open(imgpath)
                            img.load()

                            imgs.append(img)

                            os.remove(imgpath)

                res = await ai.send(msg.content, msg.author.id, msg.author.name, imgs)

            if isinstance(res, Exception):
                logger.error(str(res))
                await msg.reply(f"```\n{str(res)}```")
                return

            await msg.reply(str(res["response"]))
            self.db.add_msg(
                f"<@{msg.author.id}> ({msg.author.name}): {msg.content}\nCranberryBot: {res['response']}{''.join(res['images'])}",
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
