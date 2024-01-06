from typing import Callable
from db import DB
import discord, constants


class RPSP1Button(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        p1_id: int,
        init_p2: Callable,
    ) -> None:
        self.this_choice = this_choice
        self.p1_id = p1_id
        self.init_p2 = init_p2

        if self.this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self.this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.p1_id:
            await interaction.response.send_message(
                constants.WAIT_FOR_YOUR_TURN, ephemeral=True
            )

            return

        await self.init_p2(self.this_choice)
        await interaction.response.send_message("aight :thumbsup:", ephemeral=True)


class RPSP2Button(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        p1_id: int,
        p2_id: int,
        p1_choice: int,
    ) -> None:
        self.this_choice = this_choice
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1_choice = p1_choice

        if self.this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self.this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        view: P2View = self.view

        if interaction.user.id != self.p2_id:
            await interaction.response.send_message(
                constants.YOUR_TURN_HAS_ALREADY_PASSED, ephemeral=True
            )

            return

        new_view = discord.ui.View()

        new_view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        new_view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        new_view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        if self.this_choice == self.p1_choice:
            await interaction.response.edit_message(
                content=constants.GAME_TIE, view=view
            )
        elif (
            self.this_choice == constants.ROCK and self.p1_choice == constants.SCISSORS
        ):
            view.db.add_win("rps-pvp", self.p2_id)
            await interaction.response.edit_message(
                content=f"<@{self.p2_id}>'s rock breaks <@{self.p1_id}>'s scissor | <@{self.p2_id}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.p1_choice == constants.PAPER
        ):
            view.db.add_win("rps-pvp", self.p2_id)
            await interaction.response.edit_message(
                content=f"<@{self.p2_id}>'s scissors cuts <@{self.p1_id}>'s paper | <@{self.p2_id}> WINS!",
                view=new_view,
            )
        elif self.this_choice == constants.PAPER and self.p1_choice == constants.ROCK:
            view.db.add_win("rps-pvp", self.p2_id)
            await interaction.response.edit_message(
                content=f"<@{self.p2_id}>'s paper covers <@{self.p1_id}>'s rock | <@{self.p2_id}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.p1_choice == constants.ROCK
        ):
            view.db.add_win("rps-pvp", self.p1_id)
            await interaction.response.edit_message(
                content=f"<@{self.p1_id}>'s rock breaks <@{self.p2_id}>'s scissors | <@{self.p1_id}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.PAPER and self.p1_choice == constants.SCISSORS
        ):
            view.db.add_win("rps-pvp", self.p1_id)
            await interaction.response.edit_message(
                content=f"<@{self.p1_id}>'s scissors cut <@{self.p2_id}>'s paper | <@{self.p1_id}> WINS!",
                view=new_view,
            )
        elif self.this_choice == constants.ROCK and self.p1_choice == constants.PAPER:
            view.db.add_win("rps-pvp", self.p1_id)
            await interaction.response.edit_message(
                content=f"<@{self.p1_id}>'s paper covers <@{self.p2_id}>'s rock | <@{self.p1_id}> WINS!",
                view=new_view,
            )


class P2View(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        msg: discord.Message,
        p1_id: int,
        p2_id: int,
        p1_choice: int,
    ) -> None:
        self.msg = msg
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1_choice = p1_choice
        self.db = DB()

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSP2Button(
                    this_choice=i,
                    p1_id=self.p1_id,
                    p2_id=self.p2_id,
                    p1_choice=self.p1_choice,
                )
            )


class RPSPVPGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        msg: discord.Message,
        p1_id: int,
        p2_id: int,
    ) -> None:
        self.msg = msg
        self.p1_id = p1_id
        self.p2_id = p2_id

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSP1Button(
                    this_choice=i,
                    p1_id=self.p1_id,
                    init_p2=self.init_p2,
                )
            )

    async def init_p2(self, p1_choice: int) -> None:
        self.stop()
        await self.msg.edit(
            content=f"Now it's <@{self.p2_id}>'s turn",
            view=P2View(
                timeout=self.timeout,
                msg=self.msg,
                p1_id=self.p1_id,
                p2_id=self.p2_id,
                p1_choice=p1_choice,
            ),
        )

    async def on_timeout(self) -> None:
        view = discord.ui.View()

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        await self.msg.edit(content=constants.RPS_TIMEOUT, view=view)
