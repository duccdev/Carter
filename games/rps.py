from discord.ext import commands
import discord, tools.random, tools.db, constants, config


class RPSButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_choice: int,
        ai_choice: int,
        ctx: commands.Context,
    ) -> None:
        self.this_choice = this_choice
        self.ai_choice = ai_choice
        self.ctx = ctx

        if self.this_choice == constants.ROCK:
            super().__init__(style=style, emoji="🪨")
        elif self.this_choice == constants.PAPER:
            super().__init__(style=style, emoji="🧻")
        else:
            super().__init__(style=style, emoji="✂️")

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        view: RPSGame = self.view

        if self.ctx.author != interaction.user:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION, ephemeral=True
            )

            return

        new_view = discord.ui.View()

        new_view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        new_view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        new_view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        if self.this_choice == self.ai_choice:
            await interaction.response.edit_message(
                content=constants.GAME_TIE, view=new_view
            )
        elif (
            self.this_choice == constants.ROCK and self.ai_choice == constants.SCISSORS
        ):
            await tools.db.add_win("rps", interaction.guild, interaction.user)
            await interaction.response.edit_message(
                content=f"your rock breaks my scissor {constants.RPS_WIN}",
                view=new_view,
            )
        elif (
            self.this_choice == constants.SCISSORS and self.ai_choice == constants.PAPER
        ):
            await tools.db.add_win("rps", interaction.guild, interaction.user)
            await interaction.response.edit_message(
                content=f"your scissors cut my paper {constants.RPS_WIN}",
                view=view,
            )
        elif self.this_choice == constants.PAPER and self.ai_choice == constants.ROCK:
            await tools.db.add_win("rps", interaction.guild, interaction.user)
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

        view.stop()


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
        self.msg = msg

        super().__init__(timeout=timeout)

        for i in range(3):
            self.add_item(
                RPSButton(
                    this_choice=i,
                    ai_choice=self.ai_choice,
                    ctx=self.ctx,
                )
            )

    async def on_timeout(self) -> None:
        view = discord.ui.View(timeout=1)

        view.add_item(discord.ui.Button(emoji="🪨", disabled=True))
        view.add_item(discord.ui.Button(emoji="🧻", disabled=True))
        view.add_item(discord.ui.Button(emoji="✂️", disabled=True))

        await self.msg.edit(content=constants.RPS_TIMEOUT, view=view)
