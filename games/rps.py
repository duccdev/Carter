from typing import Callable
from discord.ext.commands import Context
import discord, tools, db, constants, config


class RPSButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        ai_choice: int,
        ctx: Context,
        db: db.DB,
        kill_view: Callable,
    ) -> None:
        self._this_choice = this_choice
        self._ai_choice = ai_choice
        self._ctx = ctx
        self._db = db
        self._kill_view = kill_view

        if self._this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self._this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        if self._ctx.author != interaction.user:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION, ephemeral=True
            )

            return

        if config.IMPOSSIBLE_GAMES:
            if self._this_choice != self._ai_choice:
                if (
                    self._this_choice == constants.ROCK
                    and self._ai_choice == constants.SCISSORS
                ):
                    self._ai_choice = constants.PAPER
                elif (
                    self._this_choice == constants.SCISSORS
                    and self._ai_choice == constants.PAPER
                ):
                    self._ai_choice = constants.ROCK
                elif (
                    self._this_choice == constants.PAPER
                    and self._ai_choice == constants.ROCK
                ):
                    self._ai_choice = constants.SCISSORS

        view = discord.ui.View(timeout=1)

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        if self._this_choice == self._ai_choice:
            await interaction.response.edit_message(
                content=constants.RPS_TIE, view=view
            )
        elif (
            self._this_choice == constants.ROCK
            and self._ai_choice == constants.SCISSORS
        ):
            self._db.load()
            self._db.add_win("rps", self._ctx.author.id)
            self._db.save()
            await interaction.response.edit_message(
                content=f"your rock breaks my scissor {constants.RPS_WIN}",
                view=view,
            )
        elif (
            self._this_choice == constants.SCISSORS
            and self._ai_choice == constants.PAPER
        ):
            self._db.load()
            self._db.add_win("rps", self._ctx.author.id)
            self._db.save()
            await interaction.response.edit_message(
                content=f"your scissors cut my paper {constants.RPS_WIN}",
                view=view,
            )
        elif self._this_choice == constants.PAPER and self._ai_choice == constants.ROCK:
            self._db.load()
            self._db.add_win("rps", self._ctx.author.id)
            self._db.save()
            await interaction.response.edit_message(
                content=f"your paper covers my rock {constants.RPS_WIN}",
                view=view,
            )
        elif (
            self._this_choice == constants.SCISSORS
            and self._ai_choice == constants.ROCK
        ):
            await interaction.response.edit_message(
                content=f"my rock breaks your scissors {constants.RPS_LOSE}",
                view=view,
            )
        elif (
            self._this_choice == constants.PAPER
            and self._ai_choice == constants.SCISSORS
        ):
            await interaction.response.edit_message(
                content=f"my scissors cut your paper {constants.RPS_LOSE}",
                view=view,
            )
        elif self._this_choice == constants.ROCK and self._ai_choice == constants.PAPER:
            await interaction.response.edit_message(
                content=f"my paper covers your rock {constants.RPS_LOSE}",
                view=view,
            )

        self._kill_view()


class RPSGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 15,
        ctx: Context,
        db: db.DB,
        msg: discord.Message,
    ) -> None:
        self._ai_choice = tools.random.randint(0, 2)
        self._ctx = ctx
        self._db = db
        self._msg = msg

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSButton(
                    this_choice=i,
                    ai_choice=self._ai_choice,
                    ctx=self._ctx,
                    db=self._db,
                    kill_view=self.stop,
                )
            )

    async def on_timeout(self) -> None:
        view = discord.ui.View(timeout=1)

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        await self._msg.edit(content=constants.RPS_TIMEOUT, view=view)
