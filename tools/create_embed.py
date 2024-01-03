from discord import Embed, Color


def createEmbed(embed_template: dict):
    embed = Embed(title=embed_template.get("title", "Embed"), color=Color.random())

    if embed_template.get("description"):
        embed.description = embed_template["description"]

    if embed_template.get("footer"):
        embed.set_footer(text=embed_template["footer"])

    for field in embed_template.get("fields", []):
        embed.add_field(name=field["name"], value=field["content"], inline=False)

    return embed
