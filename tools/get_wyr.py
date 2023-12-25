import aiohttp
import config


async def get_wyr() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            config.WYR_ROUTE,
            headers={
                "X-RapidAPI-Key": config.RAPIDAPI_KEY,
                "X-RapidAPI-Host": config.WYR_HOST,
            },
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            return body[0]["question"]
