import yaml, traceback, discord, config, constants, google.generativeai as genai

genai.configure(api_key=config.GENAI)

gemini_pro = genai.GenerativeModel("gemini-pro")
gemini_pro_vision = genai.GenerativeModel("gemini-pro-vision")


async def msgyaml_histyml(
    msg: discord.Message, bot_user: discord.ClientUser
) -> tuple[str, str]:
    msgyaml = yaml.dump(
        {
            "sender": {
                "id": msg.author.id,
                "mention": f"<@{msg.author.id}>",
                "display_name": msg.author.display_name,
                "username": msg.author.name,
            },
            "channel_name": (
                msg.channel.name or msg.author.display_name
                if not isinstance(msg.channel, discord.DMChannel)
                else msg.author.display_name
            ),
            "content": msg.content,
            "sent_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    history = []

    async for history_msg in msg.channel.history(limit=constants.CHANNEL_SEARCH_LIMIT):
        if history_msg.content.startswith(f"{config.BOT_PREFIX}ai-reset"):
            break

        if bot_user in history_msg.mentions or history_msg.author.id == bot_user.id:
            history.append(
                {
                    "sender": {
                        "id": history_msg.author.id,
                        "mention": f"<@{history_msg.author.id}>",
                        "display_name": history_msg.author.display_name,
                        "username": history_msg.author.name,
                    },
                    "channel_name": (
                        history_msg.channel.name or history_msg.author.display_name
                        if not isinstance(history_msg.channel, discord.DMChannel)
                        else history_msg.author.display_name
                    ),
                    "content": history_msg.content,
                    "sent_at": history_msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    histyml = yaml.dump(history)

    return msgyaml, histyml


async def count(msg: discord.Message, bot_user: discord.ClientUser) -> tuple[int, int]:
    msgyaml, histyml = await msgyaml_histyml(msg, bot_user)

    prompt = (
        constants.GEMINI_PRO_PROMPT
        + "Message:\n"
        + msgyaml
        + "\nMessage history:\n"
        + histyml
    )

    return len(prompt), (await gemini_pro.count_tokens_async(prompt)).total_tokens


async def send(msg: discord.Message, bot_user: discord.ClientUser) -> str:
    try:
        msgyaml, histyml = await msgyaml_histyml(msg, bot_user)

        return (
            await gemini_pro.generate_content_async(
                (
                    constants.GEMINI_PRO_PROMPT
                    + "Message:\n"
                    + msgyaml
                    + "\nMessage history:\n"
                    + histyml
                ),
                safety_settings=constants.AI_SAFETY_SETTINGS,
                generation_config=constants.AI_GENERATION_CONFIG,
            )
        ).text
    except ValueError:
        return "`Message blocked by AI provider`"
    except:
        return f"```py\n{traceback.format_exc()}```"
