from typing import Any
from discord.ext.commands import Context
import discord
import secrets
import tools


class CupButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_cup: int,
        correct_cup: int,
        slurs: list[str] = [
            "NIGGA",
            "NIGGER",
            "RETARD",
            "CHING CHONG",
            "CHINK",
            "CHINKY",
        ],
        ctx: Context,
    ) -> None:
        self._this_cup = this_cup
        self._correct_cup = correct_cup
        self._slurs = slurs
        self._ctx = ctx

        super().__init__(
            style=style,
            label=str(self._this_cup),
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        assert self.view is not None

        if self._ctx.author != interaction.user:
            await interaction.response.send_message(
                f"{'LIL ' if tools.randbool() else ''}{secrets.choice(self._slurs)} THIS ISNT YOUR GAME",
                ephemeral=True,
            )

        if self._this_cup == self._correct_cup:
            await interaction.response.edit_message(
                content=f"ok good job, it was indeed {self._this_cup} :thumbsup:",
                view=None,
            )

            return

        await interaction.response.edit_message(
            content=f"{'LIL ' if tools.randbool() else ''}{secrets.choice(self._slurs)} IT WAS {self._correct_cup} DUMBASS",
            view=None,
        )


class CupGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 15,
        cups: list[discord.ButtonStyle] = [
            discord.ButtonStyle.red,
            discord.ButtonStyle.green,
            discord.ButtonStyle.blurple,
        ],
        ctx: Context,
    ) -> None:
        self._correct_cup = tools.randint(1, len(cups))
        self._ctx = ctx

        super().__init__(timeout=timeout)

        for i in range(len(cups)):
            self.add_item(
                CupButton(
                    style=cups[i],
                    this_cup=(i + 1),
                    correct_cup=self._correct_cup,
                    ctx=self._ctx,
                )
            )
