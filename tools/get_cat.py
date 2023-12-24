import aiohttp
import config
from io import BytesIO
from os.path import basename, splitext


async def get_cat() -> tuple[BytesIO, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            config.CATS_ROUTE,
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
