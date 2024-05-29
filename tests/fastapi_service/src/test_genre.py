from http import HTTPStatus

import pytest
from faker import Faker

from tests.fastapi_service.settings import config
from tests.fastapi_service.testdata.genre import STATIC_GENRE_ID, genre_data

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer, expected_data",
    [
        (
                {
                    "page_number": 1,
                    "page_size": 50,
                },
                {"status": HTTPStatus.OK, "length": 50},
                genre_data,
        ),
        (
                {
                    "page_size": 50,
                },
                {"status": HTTPStatus.OK, "length": 50},
                genre_data,
        ),
        (
                {
                    "page_number": 1,
                },
                {"status": HTTPStatus.OK, "length": 50},
                genre_data,
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_genres_data")
async def test_genres(make_get_request, query_data, expected_answer, expected_data):
    """
    Genres list
    """
    url = config.infra.api.dsn + "/api/v1/genres"
    body, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    if expected_data:
        for genre_response in body:
            genre_id = genre_response["uuid"]
            expected_genre_list = [genre for genre in expected_data if genre["id"] == genre_id]
            assert (
                    len(expected_genre_list) == 1
            ), f"Genre with ID {genre_id} not found or multiple found in expected data."
            expected_genre = expected_genre_list[0]
            assert genre_response["name"] == expected_genre["name"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_GENRE_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_genre_by_uuid(make_get_request, uuid, expected_status):
    """
    Specific genre
    """
    url = config.infra.api.dsn + "/api/v1/genres/" + uuid
    body, _, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (fake.uuid4(), HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_genre_not_found_by_uuid(make_get_request, uuid, expected_status):
    """Genre not found"""
    url = config.infra.api.dsn + "/api/v1/genres/" + uuid
    _, _, status = await make_get_request(url)

    assert status == expected_status


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_GENRE_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_genre_by_uuid_from_cache(make_get_request, uuid, expected_status):
    """Genre by uuid from cache"""
    url = config.infra.api.dsn + "/api/v1/genres/" + uuid

    body, _, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid
