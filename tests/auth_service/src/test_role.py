import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "expected_status",
    [
        pytest.param(201, id="Valid role creation"),
        pytest.param(409, id="Duplicate role creation"),
    ],
)
async def test_create_role(create_role, expected_status):
    role_id, role_name, role_description, status, cookies = await create_role()
    assert status == expected_status


async def test_update_role(create_role, update_role):
    role_id, role_name, role_description, status, cookies = await create_role(
        role_name="example role 2", role_description="Example role description 2"
    )
    assert status == 201
    assert role_id is not None

    new_name = "Updated role name"
    new_description = "Updated role description"
    body, headers, status, cookies = await update_role(
        role_id=role_id, new_name=new_name, new_description=new_description
    )
    assert status == 200
    assert body["description"] == new_description
    assert body["name"] == new_name


async def test_delete_role(create_role, delete_role):
    role_id, role_name, role_description, status, cookies = await create_role(
        role_name="example role 3", role_description="Example role description 3"
    )
    assert status == 201
    assert role_id is not None

    body, headers, status, cookies = await delete_role(role_id)
    assert status == 200

    fake_role_id = "1c1b9a0a-1bf9-40a5-be11-847c7a27fba5"
    body, headers, status, cookies = await delete_role(fake_role_id)
    assert status == 404


async def test_list_roles(make_get_request, get_api_uri, superuser_login):
    body, headers, status, cookies = await superuser_login()
    list_url = f"{get_api_uri}/role/list"
    body, headers, status, cookies = await make_get_request(list_url, cookies=cookies)
    assert status == 200
    assert body["total_items"] == 4
