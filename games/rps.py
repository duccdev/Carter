from typing import Callable
from discord.ext import commands
from db import DB
import discord, tools, constants, config


class RPSButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        ai_choice: int,
        ctx: commands.Context,
        stop_view: Callable,
    ) -> None:
        self.this_choice = this_choice
        self.ai_choice = ai_choice
        self.ctx = ctx
        self.db = DB()
        self.stop_view = stop_view

        if self.this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self.this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.ctx.author != interaction.user:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION, ephemeral=True
            )

            return

        if config.IMPOSSIBLE_GAMES:
            if self.this_choice != self.ai_choice:
                if (
                    self.this_choice == constants.ROCK
                    and self.ai_choice == constants.SCISSORS
                ):
                    self.ai_choice = constants.PAPER
                elif (
                    self.this_choice == constants.SCISSORS
                    and self.ai_choice == constants.PAPER
                ):
                    self.ai_choice = constants.ROCK
                elif (
                    self.this_choice == constants.PAPER
                    and self.ai_choice == constants.ROCK
                ):
                    self.ai_choice = constants.SCISSORS

        view = discord.ui.View()

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        if self.this_choice == self.ai_choice:
            await interaction.response.edit_message(
                content=constants.GAME_TIE, view=view
            )
        elif (
            self.this_choice == constants.ROCK and self.ai_choice == constants.SCISSORS
        ):
            self.db.addWin("rps", self.ctx.author.id)
            await interaction.response.edit_message(
                content=f"your rock breaks my scissor {constants.RPS_WIN}",
                view=view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.ai_choice == constants.PAPER
        ):
            self.db.addWin("rps", self.ctx.author.id)
            await interaction.response.edit_message(
                content=f"your scissors cut my paper {constants.RPS_WIN}",
                view=view,
            )
        elif self.this_choice == constants.PAPER and self.ai_choice == constants.ROCK:
            self.db.addWin("rps", self.ctx.author.id)
            await interaction.response.edit_message(
                content=f"your paper covers my rock {constants.RPS_WIN}",
                view=view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.ai_choice == constants.ROCK
        ):
            await interaction.response.edit_message(
                content=f"my rock breaks your scissors {constants.RPS_LOSE}",
                view=view,
            )
        elif (
            self.this_choice == constants.PAPER and self.ai_choice == constants.SCISSORS
        ):
            await interaction.response.edit_message(
                content=f"my scissors cut your paper {constants.RPS_LOSE}",
                view=view,
            )
        elif self.this_choice == constants.ROCK and self.ai_choice == constants.PAPER:
            await interaction.response.edit_message(
                content=f"my paper covers your rock {constants.RPS_LOSE}",
                view=view,
            )

        self.stop_view()


class RPSGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        ctx: commands.Context,
        msg: discord.Message,
    ) -> None:
        self.ai_choice = tools.random.randint(0, 2)
        self.ctx = ctx
        self.db = DB()
        self.msg = msg

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSButton(
                    this_choice=i,
                    ai_choice=self.ai_choice,
                    ctx=self.ctx,
                    stop_view=self.stop,
                )
            )

    async def on_timeout(self) -> None:
        view = discord.ui.View(timeout=1)

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        await self.msg.edit(content=constants.RPS_TIMEOUT, view=view)
