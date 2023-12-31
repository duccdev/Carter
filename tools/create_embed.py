from discord import Embed, Color


def create_embed(embed_template: dict):
    embed = Embed(title=embed_template.get("title", "Embed"), color=Color.random())

    if embed_template.get("description"):
        embed.description = embed_template["description"]

    for field in embed_template.get("fields", []):
        embed.add_field(name=field["name"], value=field["content"], inline=False)

    return embed
