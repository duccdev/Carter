import discord, constants, tools.db


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

        async def game_ended() -> bool:
            content: str | None = None
            winner = view.check_winner()

            if winner:
                match winner:
                    case constants.TTT_X:
                        content = f"<@{view.player_x.id}> wins!"
                        await tools.db.add_win(
                            "tictactoe", interaction.guild, view.player_x
                        )
                    case constants.TTT_O:
                        content = f"<@{view.player_o.id}> wins!"
                        await tools.db.add_win(
                            "tictactoe", interaction.guild, view.player_o
                        )
                    case constants.TTT_TIE:
                        content = "It's a tie!"

                for child in view.children:
                    child.disabled = True

                view.stop()
                await interaction.response.edit_message(content=content, view=view)

            return winner is not None

        if interaction.user.id != view.current_turn:
            await interaction.response.send_message(
                constants.WAIT_FOR_YOUR_TURN, ephemeral=True
            )
            return

        if self.disabled:
            await interaction.response.send_message(
                constants.TTT_OCCUPIED, ephemeral=True
            )
            return

        view.board[self.y][self.x] = (
            constants.TTT_X
            if view.current_turn == view.player_x.id
            else constants.TTT_O
        )
        self.emoji = "❌" if view.current_turn == view.player_x else "⭕"
        self.disabled = True
        view.current_turn = (
            view.player_x.id
            if view.current_turn == view.player_o.id
            else view.player_o.id
        )

        if await game_ended():
            return

        await interaction.response.edit_message(
            content=f"It's <@{view.current_turn}>'s turn", view=view
        )


class TicTacToe(discord.ui.View):
    children: list[TTTButton]

    def __init__(
        self,
        *,
        timeout: float | None = 180,
        player_x: discord.Member,
        player_o: discord.Member,
    ) -> None:
        self.player_x = player_x
        self.player_o = player_o
        self.current_turn = player_x.id
        self.turn = constants.TTT_X
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
