from discord.ext import commands
from discord import Embed, Color, Message, TextChannel
from emoji import is_emoji
from db import DB
import constants, tools, ai, os, PIL.Image


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = DB()

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = tools.create_embed("Help", constants.HELP_PAGE)

        if self.bot.user:  # i have to do this so python wont annoy me
            embed.set_thumbnail(url=self.bot.user.display_avatar)

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.typing()
        await ctx.reply(f":ping_pong: `{tools.ping()}`")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def poll(
        self,
        ctx: commands.Context,
        channel: TextChannel | None,
        poll: str | None,
        *args,
    ) -> None:
        help_page = tools.create_embed("`cb!poll`", constants.POLL_HELP_PAGE)

        if not channel or not poll:
            await ctx.reply(embed=help_page)
            return

        for arg in args:
            if not is_emoji(arg):
                await ctx.reply(embed=help_page)
                return

        embed = Embed(
            title=f"Poll by {ctx.message.author.display_name}",
            description=poll,
            color=Color.random(),
        )

        msg = await channel.send(embed=embed)

        for arg in args:
            await msg.add_reaction(arg)

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

                res = (
                    await ai.send(msg.content, msg.author.id, imgs)
                    or "`prompt/response blocked for unsafe content`"
                )

            await msg.reply(res)
            self.db.load()
            self.db.add_msg(msg.content)
            self.db.add_msg(res)
            self.db.save()
            return

        self.db.load()
        self.db.add_msg(msg.content)
        self.db.save()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Other(bot))
