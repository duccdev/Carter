from typing import Callable
from discord.ext import commands
from db import DB
import discord, constants


class TTTButton(discord.ui.Button):
    def __init__(
        self,
        *,
        x: int,
        y: int,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
    ) -> None:
        self.x = x
        self.y = y

        super().__init__(style=style, label="\u200b", row=self.y)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        content: str | None = None

        if interaction.user.id != view.ctx.author.id:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION, ephemeral=True
            )
            return

        view.board[self.y][self.x] = constants.TTT_X
        self.emoji = "❌"
        self.disabled = True

        winner = view.check_winner()

        if winner:
            match winner:
                case constants.TTT_X:
                    content = "X wins!"
                case constants.TTT_O:
                    content = "O wins!"

            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.response.edit_message(content=content, view=view)

            return

        await interaction.response.edit_message(view=view)


class TicTacToe(discord.ui.View):
    children: list[TTTButton]

    def __init__(
        self,
        *,
        timeout: float | None = 180,
        ctx: commands.Context,
    ) -> None:
        self.ctx = ctx
        self.db = DB()
        self.board = [
            [constants.TTT_EMPTY, constants.TTT_EMPTY, constants.TTT_EMPTY],
            [constants.TTT_EMPTY, constants.TTT_EMPTY, constants.TTT_EMPTY],
            [constants.TTT_EMPTY, constants.TTT_EMPTY, constants.TTT_EMPTY],
        ]

        super().__init__(timeout=timeout)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.add_item(TTTButton(x=x, y=y))

    def check_winner(self) -> int | None:
        possible_winners = [constants.TTT_X, constants.TTT_O]

        # check horizontal
        for winner in possible_winners:
            for y in range(3):
                if (
                    self.board[y][0] == winner
                    and self.board[y][1] == winner
                    and self.board[y][2] == winner
                ):
                    return winner

        # check vertical
        for winner in possible_winners:
            for x in range(3):
                if (
                    self.board[0][x] == winner
                    and self.board[1][x] == winner
                    and self.board[2][x] == winner
                ):
                    return winner

        # check diagonal
        for winner in possible_winners:
            if (
                self.board[0][0] == winner
                and self.board[1][1] == winner
                and self.board[2][2] == winner
            ) or (
                self.board[2][0] == winner
                and self.board[1][1] == winner
                and self.board[0][2] == winner
            ):
                return winner

        # check tie
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == constants.TTT_EMPTY:
                    return None

        return constants.TTT_TIE
