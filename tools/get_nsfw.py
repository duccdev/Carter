import aiohttp
import config
from io import BytesIO
from os.path import basename, splitext


class NsfwNotFoundError(Exception):
    pass


async def get_nsfw(category: str, content_type: str) -> tuple[BytesIO, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.nsfw_route(category, content_type)) as response:
            if response.status == 404 or response.status == 403:
                raise NsfwNotFoundError()

            if response.status != 200:
                raise Exception((await response.json()))

            body = await response.json()
            link = body["link"]

            async with session.get(link) as response:
                if response.status != 200:
                    raise Exception()

                return BytesIO(await response.read()), splitext(basename(link))[1]
