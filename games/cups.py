from typing import Callable
from discord.ext.commands import Context
import discord, tools, db, constants, config


class CupButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_cup: int,
        correct_cup: int,
        cups: list[discord.ButtonStyle],
        ctx: Context,
        db: db.DB,
        kill_view: Callable,
    ) -> None:
        self.this_cup = this_cup
        self.correct_cup = correct_cup
        self.cups = cups
        self.ctx = ctx
        self.db = db
        self.kill_view = kill_view

        super().__init__(
            style=style,
            emoji="<:cup:1189263945744261121>",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.ctx.author != interaction.user:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION,
                ephemeral=True,
            )

            return

        view = discord.ui.View(timeout=1)

        if config.IMPOSSIBLE_GAMES:
            while self.this_cup == self.correct_cup:
                self.correct_cup = tools.random.randint(0, len(self.cups) - 1)

        for i in range(len(self.cups)):
            if self.correct_cup == i:
                view.add_item(
                    discord.ui.Button(
                        style=self.cups[i],
                        emoji="🥎",
                        disabled=True,
                    )
                )

                continue

            if self.this_cup == i and self.correct_cup != i:
                view.add_item(
                    discord.ui.Button(
                        style=self.cups[i],
                        emoji="❌",
                        disabled=True,
                    )
                )

                continue

            view.add_item(
                discord.ui.Button(
                    style=self.cups[i],
                    emoji="<:cup:1189263945744261121>",
                    disabled=True,
                )
            )

        if self.this_cup == self.correct_cup:
            await interaction.response.edit_message(
                content=f"ok good job, it was indeed cup {self.this_cup + 1} :thumbsup:",
                view=view,
            )

            self.kill_view()

            self.db.add_win(
                "cups",
                interaction.user.id,
            )

            return

        await interaction.response.edit_message(
            content=f"no you dumbass, it was {self.correct_cup + 1}",
            view=view,
        )

        self.kill_view()


class Cups(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 15,
        cups: list[discord.ButtonStyle] = [
            discord.ButtonStyle.red,
            discord.ButtonStyle.green,
            discord.ButtonStyle.blurple,
        ],
        ctx: Context,
        db: db.DB,
        msg: discord.Message,
    ) -> None:
        self.cups = cups
        self.correct_cup = tools.random.randint(0, len(self.cups) - 1)
        self.ctx = ctx
        self.db = db
        self.msg = msg

        super().__init__(timeout=timeout)

        for i in range(len(self.cups)):
            self.add_item(
                CupButton(
                    style=self.cups[i],
                    this_cup=i,
                    correct_cup=self.correct_cup,
                    ctx=self.ctx,
                    db=self.db,
                    cups=self.cups,
                    kill_view=self.stop,
                )
            )

    async def on_timeout(self) -> None:
        view = discord.ui.View(timeout=1)

        for i in range(len(self.cups)):
            view.add_item(
                discord.ui.Button(
                    style=self.cups[i],
                    emoji="<:cup:1189263945744261121>",
                    disabled=True,
                )
            )

        await self.msg.edit(
            content=constants.CUPS_TIMEOUT,
            view=view,
        )
