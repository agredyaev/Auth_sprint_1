from typing import Any

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
def user_credentials():
    from tests.auth_service.settings import config

    return {
        "superuser": {"email": config.su.email, "password": config.su.password},
        "default_user": {"email": "defaultuser@example.com", "password": "strongpassword123"},
        "default_user_new_pass": {"email": "defaultuser@example.com", "password": "newstrongpassword123"},
        "second_default_user": {"email": "second_defaultuser@example.com", "password": "strongpassword123"},
        "login_history_user": {"email": "historyuser@example.com", "password": "strongpassword123"},
    }


@pytest_asyncio.fixture(scope="module")
async def login_user(make_post_request, get_api_uri):
    async def login(payload: dict[str, Any]):
        login_url = f"{get_api_uri}/user/login"
        body, headers, status, cookies = await make_post_request(url=login_url, form_data=payload)
        return body, headers, status, cookies

    return login


@pytest_asyncio.fixture(scope="module")
async def superuser_login(login_user, user_credentials):
    async def login():
        return await login_user(user_credentials.get("superuser"))

    return login


@pytest_asyncio.fixture(scope="module")
async def logout_user(make_post_request, get_api_uri):
    async def logout(cookies: dict[str, Any]):
        logout_url = f"{get_api_uri}/user/logout"
        body, headers, status, cookies = await make_post_request(url=logout_url, cookies=cookies)
        return body, headers, status, cookies

    return logout


@pytest_asyncio.fixture(scope="module")
async def create_user(make_post_request, get_api_uri):
    async def create(payload: dict[str, Any]):
        url = f"{get_api_uri}/user/signup"
        body, headers, status, cookies = await make_post_request(url=url, form_data=payload)
        user_id = body["id"]
        return user_id, body, headers, status, cookies

    return create


@pytest_asyncio.fixture(scope="module")
async def create_default_user(create_user, user_credentials):
    user_id, body, headers, status, cookies = await create_user(user_credentials.get("default_user"))
    return user_id


@pytest_asyncio.fixture(scope="module")
async def default_user_login(login_user, user_credentials):
    async def login():
        return await login_user(user_credentials.get("default_user"))

    return login
