import constants, aiohttp


async def get_nhie(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{constants.NEVER_HAVE_I_EVER_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]
