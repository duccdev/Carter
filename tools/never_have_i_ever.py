import aiohttp
import config


async def neverHaveIEver(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.NEVER_HAVE_I_EVER_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]
