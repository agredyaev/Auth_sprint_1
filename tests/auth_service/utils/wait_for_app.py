import asyncio

import aiohttp
import backoff

from tests.auth_service.settings import config


async def check_nginx(session: aiohttp.ClientSession) -> None:
    async with session.get(config.infra.api.health_check) as response:
        if response.status != 200:
            raise aiohttp.ClientError("Nginx is not available. Backoff...")


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60, max_tries=50)
async def wait_for_nginx() -> None:
    async with aiohttp.ClientSession() as session:
        await check_nginx(session)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(wait_for_nginx())
    finally:
        loop.close()
