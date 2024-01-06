import aiohttp, config, constants
from io import BytesIO
from os.path import basename, splitext


async def get_cat() -> tuple[BytesIO, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            constants.CATS_ROUTE,
            headers={"x-api-key": config.CAT_API_KEY},
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            cat_url = body[0]["url"]

            async with session.get(cat_url) as response:
                if response.status != 200:
                    raise Exception()

                return BytesIO(await response.read()), splitext(basename(cat_url))[1]


async def get_dog() -> tuple[BytesIO, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            constants.DOGS_ROUTE,
            headers={"x-api-key": config.DOG_API_KEY},
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            cat_url = body[0]["url"]

            async with session.get(cat_url) as response:
                if response.status != 200:
                    raise Exception()

                return BytesIO(await response.read()), splitext(basename(cat_url))[1]


async def get_fact() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(constants.FACTS_ROUTE) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            return body["text"]


async def get_meme() -> tuple[str, BytesIO, str, bool]:
    async with aiohttp.ClientSession() as session:
        async with session.get(constants.MEMES_ROUTE) as response:
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
