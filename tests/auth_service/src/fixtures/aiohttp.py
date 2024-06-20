from typing import Any

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def get_api_uri() -> str:
    from tests.auth_service.settings import config

    return f"{config.infra.api.dsn}{config.infra.api.api_path}"


@pytest_asyncio.fixture(scope="module", name="make_get_request")
def make_get_request():
    async def inner(
        url: str,
        query_data: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str], int, dict[str, Any]]:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url, params=query_data) as response:
                body = await response.json()
                headers = dict(response.headers)
                status = response.status
                cookies = dict(response.cookies)

        return body, headers, status, cookies

    return inner


@pytest_asyncio.fixture(scope="module", name="make_post_request")
def make_post_request():
    async def inner(
        url: str,
        form_data: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str], int, dict[str, Any]]:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.post(url=url, json=form_data) as response:
                body = await response.json()
                headers = dict(response.headers)
                status = response.status
                cookies = dict(response.cookies)
        return body, headers, status, cookies

    return inner
