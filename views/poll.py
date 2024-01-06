from db import DB
import discord


class PollOption(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        option: int,
        poll_id: str,
    ):
        self.db = DB()
        self.option = option
        self.poll_id = poll_id

        super().__init__(style=style, label=str(self.option))

    async def callback(self, interaction: discord.interactions.Interaction):
        self.db.set_vote(self.poll_id, interaction.user.id, self.option)

        await interaction.response.send_message(
            "Your vote has been set!", ephemeral=True
        )


class ViewVotesButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.green,
        poll_id: str,
    ):
        self.db = DB()
        self.poll_id = poll_id

        super().__init__(style=style, label="View votes", row=2)

    async def callback(self, interaction: discord.interactions.Interaction):
        votes = self.db.get_votes(self.poll_id)
        embed = discord.Embed(color=discord.Color.random(), title="Votes")

        for k, v in votes.items():
            embed.add_field(name=k, value=f"Votes: {v}")

        await interaction.response.send_message(embed=embed, ephemeral=True)


class RemoveVoteButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.danger,
        poll_id: str,
    ):
        self.db = DB()
        self.poll_id = poll_id

        super().__init__(style=style, label="Remove vote", row=2)

    async def callback(self, interaction: discord.interactions.Interaction):
        self.db.remove_vote(self.poll_id, interaction.user.id)
        await interaction.response.send_message("Done! :thumbsup:", ephemeral=True)


class Poll(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = None,
        options: list[int],
    ):
        self.db = DB()
        self.options = options
        self.poll_id = self.db.create_poll(self.options)

        super().__init__(timeout=timeout)

        for option in options:
            self.add_item(PollOption(option=option, poll_id=self.poll_id))

        self.add_item(ViewVotesButton(poll_id=self.poll_id))
        self.add_item(RemoveVoteButton(poll_id=self.poll_id))
