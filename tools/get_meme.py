import aiohttp
import config
from io import BytesIO
from os.path import basename, splitext


async def getMeme() -> tuple[str, BytesIO, str, bool]:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.MEMES_ROUTE) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            meme_title = body["title"]
            meme_url = body["url"]
            meme_nsfw = body["nsfw"]

            async with session.get(meme_url) as response:
                if response.status != 200:
                    raise Exception()

                return (
                    meme_title,
                    BytesIO(await response.read()),
                    splitext(basename(meme_url))[1],
                    meme_nsfw,
                )
