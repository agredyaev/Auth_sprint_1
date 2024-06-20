import pytest

from tests.auth_service.settings import config

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "email, password, expected_status",
    [
        pytest.param("defaultuser@example.com", "strongpassword123", 201, id="Valid user creation"),
        pytest.param("defaultuser@example.com", "strongpassword123", 409, id="Duplicate user creation"),
        pytest.param("shortpassword@example.com", "short", 422, id="Password less than 8 characters"),
        pytest.param("invalid-email", "validpassword123", 422, id="Invalid email format"),
    ],
)
async def test_user_signup(make_post_request, email, password, expected_status, get_api_uri):
    url = f"{get_api_uri}/user/signup"
    payload = {"email": email, "password": password}
    body, headers, status, cookies = await make_post_request(url, form_data=payload)
    assert status == expected_status


@pytest.mark.parametrize(
    "email, password, expected_status, token_expected",
    [
        pytest.param("defaultuser@example.com", "strongpassword123", 200, True, id="Valid email and password"),
        pytest.param("defaultuser@example.com", "invalidpassword", 401, False, id="Invalid password"),
        pytest.param("invaliduser@example.com", "strongpassword123", 401, False, id="Invalid email"),
    ],
)
async def test_user_login(make_post_request, email, password, expected_status, token_expected, get_api_uri):
    url = f"{get_api_uri}/user/login"
    payload = {"email": email, "password": password}
    body, headers, status, cookies = await make_post_request(url, form_data=payload)

    assert status == expected_status

    if token_expected:
        assert "access_token_cookie" in cookies
        assert "refresh_token_cookie" in cookies
    else:
        assert "access_token_cookie" not in cookies
        assert "refresh_token_cookie" not in cookies


@pytest.mark.parametrize(
    "new_password, old_password, expected_status, num",
    [
        pytest.param("newstrongpassword123", "strongpassword123", 200, 1, id="Correct old password"),
        pytest.param("strongpassword123", "newstrongpassword123", 200, 2, id="Correct old password rollback"),
        pytest.param("newstrongpassword123", "wrongpassword123", 401, 3, id="Incorrect old password"),
    ],
)
async def test_update_password(
    make_post_request, login_user, new_password, old_password, expected_status, get_api_uri, user_credentials, num
):
    user = "default_user_new_pass" if num == 2 else "default_user"
    body, headers, status, cookies = await login_user(user_credentials.get(user))
    print("login", body, headers, status, cookies)

    url = f"{get_api_uri}/user/password_update"
    payload = {"email": "defaultuser@example.com", "password": new_password, "old_password": old_password}

    body, headers, status, cookies = await make_post_request(url, form_data=payload, cookies=cookies)
    assert status == expected_status


@pytest.mark.parametrize(
    "refresh_token, expected_status",
    [
        pytest.param("valid", 200, id="Valid refresh token"),
        pytest.param("invalid", 401, id="Invalid refresh token"),
        pytest.param("expired", 422, id="Expired refresh token"),
    ],
)
async def test_refresh_token(
    make_post_request, default_user_login, refresh_token, expected_status, get_api_uri, flush_tokens, add_to_deny_list
):
    await flush_tokens()
    body, headers, status, cookies = await default_user_login()

    if refresh_token == "invalid":
        await add_to_deny_list()
    elif refresh_token == "expired":
        cookies["refresh_token_cookie"] = "expired"

    url = f"{get_api_uri}/user/refresh"
    body, headers, status, cookies = await make_post_request(url, cookies=cookies)
    assert status == expected_status


async def test_login_history(make_get_request, create_user, get_api_uri, user_credentials, login_user, logout_user):
    (
        user_id,
        *_,
    ) = await create_user(user_credentials.get("login_history_user"))
    *_, cookies = await login_user(user_credentials.get("login_history_user"))
    await logout_user(cookies=cookies)
    *_, cookies = await login_user(user_credentials.get("login_history_user"))

    history_url = f"{get_api_uri}/user/history"
    body, headers, status, cookies = await make_get_request(history_url, cookies=cookies)
    print(body)

    assert status == 200
    assert body["total_items"] == 2

    first_login = body["response"][0]
    second_login = body["response"][1]

    assert first_login["login_at"] is not None
    assert first_login["logout_at"] is None

    assert second_login["login_at"] is not None
    assert second_login["logout_at"] is not None


@pytest.mark.parametrize(
    "endpoint",
    [
        pytest.param("/user/role/assign", id="Assign role"),
        pytest.param("/user/role/revoke", id="Revoke role"),
        pytest.param("/user/role/verify", id="Verify role"),
        pytest.param("/role/create", id="Create role"),
        pytest.param("/role/update", id="Update role"),
        pytest.param("/role/delete", id="Delete role"),
    ],
)
async def test_admin_endpoints_access(make_post_request, default_user_login, endpoint, get_api_uri):
    body, headers, status, cookies = await default_user_login()

    url = f"{get_api_uri}{endpoint}"

    body, headers, status, cookies = await make_post_request(url, cookies=cookies)
    assert status == 403


async def test_assign_and_verify_role(make_post_request, create_user, superuser_login, get_api_uri, user_credentials):
    user_for_verify = user_credentials.get("second_default_user")
    (
        user_id,
        *_,
    ) = await create_user(user_for_verify)
    *_, cookies = await superuser_login()

    assign_url = f"{get_api_uri}/user/role/assign"
    payload = {"user_id": user_id, "roles": [{"role_id": config.su.role_id}]}

    body, _, status, _ = await make_post_request(assign_url, form_data=payload, cookies=cookies)
    assert status == 200

    verify_url = f"{get_api_uri}/user/role/verify"
    verify_payload = {"email": user_for_verify.get("email"), "role_names": [{"name": "admin"}]}
    body, _, status, _ = await make_post_request(verify_url, form_data=verify_payload, cookies=cookies)
    assert status == 200
    assert config.su.role_id in [role["id"] for role in body["roles"]]

    revoke_url = f"{get_api_uri}/user/role/revoke"
    revoke_payload = {"user_id": user_id, "roles": [{"role_id": config.su.role_id}]}
    body, _, status, _ = await make_post_request(revoke_url, form_data=revoke_payload, cookies=cookies)
    assert status == 200

    body, _, status, _ = await make_post_request(verify_url, form_data=verify_payload, cookies=cookies)
    assert status == 404
