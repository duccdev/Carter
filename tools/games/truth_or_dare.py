import constants, aiohttp


async def get_truth(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{constants.TRUTH_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]


async def get_dare(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{constants.DARE_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]
