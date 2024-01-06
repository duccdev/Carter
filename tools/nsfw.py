import aiohttp
from io import BytesIO
from os.path import basename, splitext


class NsfwNotFoundError(Exception):
    pass


def nsfw_route(category: str, content_type: str) -> str:
    return f"https://purrbot.site/api/img/nsfw/{category}/{content_type}"


async def get_nsfw(category: str, content_type: str) -> tuple[BytesIO, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(nsfw_route(category, content_type)) as response:
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
