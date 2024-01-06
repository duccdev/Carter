from typing import Callable
from discord.ext import commands
from db import DB
import discord, tools.random, constants, config


class CupButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_cup: int,
        correct_cup: int,
        cups: list[discord.ButtonStyle],
        ctx: commands.Context,
    ) -> None:
        self.this_cup = this_cup
        self.correct_cup = correct_cup
        self.cups = cups
        self.ctx = ctx

        super().__init__(
            style=style,
            emoji="<:cup:1189263945744261121>",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        view: Cups = self.view
        new_view = discord.ui.View()

        if self.ctx.author != interaction.user:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION,
                ephemeral=True,
            )

            return

        if config.IMPOSSIBLE_GAMES:
            while self.this_cup == self.correct_cup:
                self.correct_cup = tools.random.randint(0, len(self.cups) - 1)

        for i in range(len(self.cups)):
            if self.correct_cup == i:
                new_view.add_item(
                    discord.ui.Button(
                        style=self.cups[i],
                        emoji="🥎",
                        disabled=True,
                    )
                )

                continue

            if self.this_cup == i and self.correct_cup != i:
                new_view.add_item(
                    discord.ui.Button(
                        style=self.cups[i],
                        emoji="❌",
                        disabled=True,
                    )
                )

                continue

            new_view.add_item(
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

            view.stop()

            view.db.add_win(
                "cups",
                interaction.user.id,
            )

            return

        await interaction.response.edit_message(
            content=f"no you dumbass, it was {self.correct_cup + 1}",
            view=view,
        )

        view.stop()


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
        ctx: commands.Context,
        msg: discord.Message,
    ) -> None:
        self.cups = cups
        self.correct_cup = tools.random.randint(0, len(self.cups) - 1)
        self.ctx = ctx
        self.db = DB()
        self.msg = msg

        super().__init__(timeout=timeout)

        for i in range(len(self.cups)):
            self.add_item(
                CupButton(
                    style=self.cups[i],
                    this_cup=i,
                    correct_cup=self.correct_cup,
                    ctx=self.ctx,
                    cups=self.cups,
                )
            )

    async def on_timeout(self) -> None:
        new_view = discord.ui.View()

        for i in range(len(self.cups)):
            new_view.add_item(
                discord.ui.Button(
                    style=self.cups[i],
                    emoji="<:cup:1189263945744261121>",
                    disabled=True,
                )
            )

        await self.msg.edit(
            content=constants.CUPS_TIMEOUT,
            view=new_view,
        )
