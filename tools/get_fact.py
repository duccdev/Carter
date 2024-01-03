import aiohttp
import config


async def getFact() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.FACTS_ROUTE) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(body)

            return body["text"]
