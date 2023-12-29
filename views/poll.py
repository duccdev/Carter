from discord.interactions import Interaction
from discord.ui import Button, View
from discord import ButtonStyle, Color, Embed, Message
from db import DB


class PollOption(Button):
    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.secondary,
        option: str,
        poll_id: str,
    ):
        self.db = DB()
        self.option = option
        self.poll_id = poll_id

        super().__init__(style=style, label=self.option)

    async def callback(self, interaction: Interaction):
        self.db.set_vote(self.poll_id, interaction.user.id, self.option)

        await interaction.response.send_message(
            "Your vote has been set!", ephemeral=True
        )


class ViewVotesButton(Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.green, poll_id: str):
        self.db = DB()
        self.poll_id = poll_id

        super().__init__(style=style, label="View votes")

    async def callback(self, interaction: Interaction):
        votes = self.db.get_votes(self.poll_id)
        embed = Embed(color=Color.random(), title="Votes")

        for k, v in votes.items():
            embed.add_field(name=k, value=f"Votes: {v}")

        await interaction.response.send_message(embed=embed, ephemeral=True)


class RemoveVoteButton(Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.danger, poll_id: str):
        self.db = DB()
        self.poll_id = poll_id

        super().__init__(style=style, label="Remove vote")

    async def callback(self, interaction: Interaction):
        self.db.remove_vote(self.poll_id, interaction.user.id)
        await interaction.response.send_message("Done! :thumbsup:", ephemeral=True)


class Poll(View):
    def __init__(
        self,
        *,
        timeout: float | None = None,
        options: list[str],
    ):
        self.db = DB()
        self.options = options
        self.poll_id = self.db.create_poll(self.options)

        super().__init__(timeout=timeout)

        for option in options:
            self.add_item(PollOption(option=option, poll_id=self.poll_id))

        self.add_item(ViewVotesButton(poll_id=self.poll_id))
        self.add_item(RemoveVoteButton(poll_id=self.poll_id))
