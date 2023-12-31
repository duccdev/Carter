import discord, constants, tools


class HelpMenu(discord.ui.Select):
    def __init__(self, sender: int) -> None:
        self.sender = sender

        super().__init__(
            placeholder="Select a page",
            options=[
                discord.SelectOption(
                    label=page["label"],
                    emoji=page["emoji"],
                    value=page["value"],
                )
                for page in [
                    {
                        "label": constants.HELP_PAGES[key]["title"].split(" ")[1],
                        "emoji": constants.HELP_PAGES[key]["title"].split(" ")[0],
                        "value": key,
                    }
                    if len(constants.HELP_PAGES[key]["title"].split(" ")) > 1
                    else {
                        "label": constants.HELP_PAGES[key]["title"],
                        "emoji": "",
                        "value": key,
                    }
                    for key in constants.HELP_PAGES
                ]
            ],
        )

    async def callback(self, interaction: discord.interactions.Interaction) -> None:
        if interaction.user.id != self.sender:
            await interaction.response.send_message(
                constants.NON_OWNER_INTERACTION, ephemeral=True
            )

            return

        await interaction.response.edit_message(
            embed=tools.create_embed(
                constants.HELP_PAGES[self.values[0]],
            ),
        )


class HelpView(discord.ui.View):
    def __init__(self, *, sender: int) -> None:
        self.sender = sender

        super().__init__(timeout=None)
        self.add_item(HelpMenu(self.sender))
