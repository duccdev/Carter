import config, constants, PIL.Image, google.generativeai as genai
from db import DB

genai.configure(api_key=config.GENAI_API_KEY)

safety_settings = {
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
    "HARM_CATEGORY_HATE_SPEECH": "block_none",
    "HARM_CATEGORY_HARASSMENT": "block_none",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
}

gemini_pro = genai.GenerativeModel("gemini-pro")
gemini_pro_vision = genai.GenerativeModel("gemini-pro-vision")

db = DB()


def construct_req(
    req: str,
    history: str,
    msg: str,
    sender_id: int,
    img: str = "",
) -> str:
    req = f"{req}\n{(history or '')}\n<@{sender_id}>: {msg}"

    if img:
        req += f"\nAttached image description:{img}"

    return req


async def send(
    msg: str,
    sender_id: int,
    img: PIL.Image.Image | None = None,
) -> str | None:
    db.load()

    prompt = constants.AI_PROMPT
    history = db.get_msg_history()
    img_desc = ""

    try:
        if img:
            img_desc = (
                await gemini_pro_vision.generate_content_async(
                    img, safety_settings=safety_settings
                )
            ).text
    except:
        pass

    reconstruct_req = lambda: construct_req(prompt, history, msg, sender_id, img_desc)

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

    db.set_msg_history(history)
    db.save()

    try:
        return (
            await gemini_pro.start_chat().send_message_async(
                req, safety_settings=safety_settings
            )
        ).text
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
