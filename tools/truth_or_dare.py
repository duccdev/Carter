import aiohttp
import config


async def getTruth(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.TRUTH_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]


async def getDare(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.DARE_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]
