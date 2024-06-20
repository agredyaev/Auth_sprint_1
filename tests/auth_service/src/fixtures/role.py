from typing import Any

import pytest
import pytest_asyncio
from faker import Faker


@pytest_asyncio.fixture(scope="module")
async def get_permissions_levels():
    return [{"level": 15}, {"level": 10}, {"level": 5}, {"level": 0}]


@pytest_asyncio.fixture(scope="module")
async def create_role(make_post_request, get_permissions_levels, get_api_uri, superuser_login):
    async def _create_role(role_name: str = "example role", role_description: str = "Example role description"):
        body, headers, status, cookies = await superuser_login()

        url = f"{get_api_uri}/role/create"
        payload = {"name": role_name, "description": role_description, "permission_levels": get_permissions_levels}
        body, headers, status, cookies1 = await make_post_request(url, form_data=payload, cookies=cookies)
        role_id = None
        if status == 201:
            role_id = body["id"]

        return role_id, role_name, role_description, status, cookies

    return _create_role


@pytest_asyncio.fixture(scope="module")
async def update_role(make_post_request, get_permissions_levels, get_api_uri, superuser_login):
    async def _update_role(role_id: str, new_name: str, new_description: str):
        body, headers, status, cookies = await superuser_login()
        url = f"{get_api_uri}/role/update"
        payload = {
            "id": role_id,
            "name": new_name,
            "description": new_description,
            "permission_levels": get_permissions_levels,
        }
        body, headers, status, cookies = await make_post_request(url=url, form_data=payload, cookies=cookies)
        return body, headers, status, cookies

    return _update_role


@pytest_asyncio.fixture(scope="function")
async def delete_role(make_post_request, get_api_uri, superuser_login):
    async def _delete_role(role_id: str):
        body, headers, status, cookies = await superuser_login()
        url = f"{get_api_uri}/role/delete"
        payload = {"id": role_id}
        body, headers, status, cookies = await make_post_request(url, form_data=payload, cookies=cookies)
        print("Deleted role", body, headers, status, cookies)
        return body, headers, status, cookies

    return _delete_role
