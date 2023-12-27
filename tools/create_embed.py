from discord import Embed, Color


def create_embed(title: str, embed_template: list[dict[str, str]]):
    embed = Embed(title=title, color=Color.random())

    for field in embed_template:
        embed.add_field(name=field["name"], value=field["content"], inline=False)

    return embed
