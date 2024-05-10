from typing import Callable, Coroutine
import discord, constants, tools.db


class RPSP1Button(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        p1: discord.Member,
        init_p2: Callable[[int], Coroutine],
    ) -> None:
        self.this_choice = this_choice
        self.p1 = p1
        self.init_p2 = init_p2

        if self.this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self.this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.p1.id:
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
        p1: discord.Member,
        p2: discord.Member,
        p1_choice: int,
    ) -> None:
        self.this_choice = this_choice
        self.p1 = p1
        self.p2 = p2
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

        if interaction.user.id != self.p2.id:
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
            await tools.db.add_win("rps-pvp", interaction.guild, self.p2)
            await interaction.response.edit_message(
                content=f"<@{self.p2}>'s rock breaks <@{self.p1}>'s scissor | <@{self.p2}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.p1_choice == constants.PAPER
        ):
            await tools.db.add_win("rps-pvp", interaction.guild, self.p2)
            await interaction.response.edit_message(
                content=f"<@{self.p2}>'s scissors cuts <@{self.p1}>'s paper | <@{self.p2}> WINS!",
                view=new_view,
            )
        elif self.this_choice == constants.PAPER and self.p1_choice == constants.ROCK:
            await tools.db.add_win("rps-pvp", interaction.guild, self.p2)
            await interaction.response.edit_message(
                content=f"<@{self.p2}>'s paper covers <@{self.p1}>'s rock | <@{self.p2}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.p1_choice == constants.ROCK
        ):
            await tools.db.add_win("rps-pvp", interaction.guild, self.p1)
            await interaction.response.edit_message(
                content=f"<@{self.p1}>'s rock breaks <@{self.p2}>'s scissors | <@{self.p1}> WINS!",
                view=new_view,
            )
        elif (
            self.this_choice == constants.PAPER and self.p1_choice == constants.SCISSORS
        ):
            await tools.db.add_win("rps-pvp", interaction.guild, self.p1)
            await interaction.response.edit_message(
                content=f"<@{self.p1}>'s scissors cut <@{self.p2}>'s paper | <@{self.p1}> WINS!",
                view=new_view,
            )
        elif self.this_choice == constants.ROCK and self.p1_choice == constants.PAPER:
            await tools.db.add_win("rps-pvp", interaction.guild, self.p1)
            await interaction.response.edit_message(
                content=f"<@{self.p1}>'s paper covers <@{self.p2}>'s rock | <@{self.p1}> WINS!",
                view=new_view,
            )


class P2View(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        msg: discord.Message,
        p1: discord.Member,
        p2: discord.Member,
        p1_choice: int,
    ) -> None:
        self.msg = msg
        self.p1 = p1
        self.p2 = p2
        self.p1_choice = p1_choice

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSP2Button(
                    this_choice=i,
                    p1=self.p1,
                    p2=self.p2,
                    p1_choice=self.p1_choice,
                )
            )


class RPSPVPGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        msg: discord.Message,
        p1: discord.Member,
        p2: discord.Member,
    ) -> None:
        self.msg = msg
        self.p1 = p1
        self.p2 = p2

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSP1Button(
                    this_choice=i,
                    p1=self.p1,
                    init_p2=self.init_p2,
                )
            )

    async def init_p2(self, p1_choice: int) -> None:
        self.stop()
        await self.msg.edit(
            content=f"Now it's <@{self.p2.id}>'s turn",
            view=P2View(
                timeout=self.timeout,
                msg=self.msg,
                p1=self.p1,
                p2=self.p2,
                p1_choice=p1_choice,
            ),
        )

    async def on_timeout(self) -> None:
        view = discord.ui.View()

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        await self.msg.edit(content=constants.RPS_TIMEOUT, view=view)
