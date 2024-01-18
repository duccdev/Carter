import tools.other, config, constants, PIL.Image, google.generativeai as genai
from db import DB

genai.configure(api_key=config.GENAI)

gemini_pro = genai.GenerativeModel("gemini-pro")
gemini_pro_vision = genai.GenerativeModel("gemini-pro-vision")

db = DB()


def construct_req(
    prompt: str,
    history: str,
    msg: str,
    author_name: str,
    author_id: int,
    img_descriptions: list[str] = [],
) -> str:
    req = f"{prompt}\n{author_name} (<@{author_id}>): {msg}\n\nMessage history:\n\n{history}"

    if img_descriptions:
        for i in range(len(img_descriptions)):
            req += f"\nAttached image #{i} description: {img_descriptions[i]}"

    return req


async def chat_send(
    msg: str,
    channel_id: int,
    author_name: str,
    author_id: int,
    imgs: list[PIL.Image.Image] = [],
) -> dict[str, str | list[str]]:
    db.load()

    history = db.get_msg_history(channel_id)
    img_descriptions: list[str] = []

    try:
        for img in imgs:
            img_descriptions.append(
                (
                    await gemini_pro_vision.generate_content_async(
                        [constants.GEMINI_PRO_VISION_PROMPT, img],
                        safety_settings=constants.AI_SAFETY_SETTINGS,
                    )
                ).text
            )
    except:
        pass

    reconstruct_req = lambda: construct_req(
        constants.GEMINI_PRO_CHAT_PROMPT,
        history,
        msg,
        author_name,
        author_id,
        img_descriptions,
    )

    req = reconstruct_req()

    while len(req) > constants.GEMINI_PRO_CHARS_LIMIT:
        history_lines = history.splitlines()

        if len(history_lines) > 10:
            history_lines.pop()
            history = "".join(history_lines)
            req = reconstruct_req()
            continue

        if len(msg) > (len(req) - constants.GEMINI_PRO_CHARS_LIMIT):
            msg = msg[: (len(req) - constants.GEMINI_PRO_CHARS_LIMIT)]
        else:
            msg = msg[: int(len(msg) / 2)]

        req = reconstruct_req()

    db.set_msg_history(channel_id, history)
    db.save()

    return {
        "response": (
            await gemini_pro.generate_content_async(
                req,
                safety_settings=constants.AI_SAFETY_SETTINGS,
                temperature=0.6,
            )
        ).text,
        "images": img_descriptions,
    }
