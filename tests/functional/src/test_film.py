from http import HTTPStatus

import pytest
from faker import Faker

from tests.functional.settings import config
from tests.functional.testdata.film import STATIC_FILM_ID, STATIC_FILM_TITLE, STATIC_GENRE

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"query": STATIC_FILM_TITLE, "page_number": 1, "page_size": 50, "sort": "-imdb_rating"},
            {"status": HTTPStatus.OK, "length": 50},
        ),
        ({"query": STATIC_FILM_TITLE, "page_number": 1, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"query": STATIC_FILM_TITLE, "page_size": 50, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"query": STATIC_FILM_TITLE, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"query": STATIC_FILM_TITLE, "sort": "imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"query": "Unknown_Name", "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 0}),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films_search(make_get_request, query_data, expected_answer):
    """
    Check films search
    """
    url = config.infra.api.dsn + "/api/v1/films/search"
    body, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_number": 1, "page_size": 50, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"page_size": 50, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"page_number": 1, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"sort": "imdb_rating"}, {"status": HTTPStatus.OK, "length": 50}),
        ({"sort": "-imdb_rating", "genre": "Unknown"}, {"status": HTTPStatus.OK, "length": 0}),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films(make_get_request, query_data, expected_answer):
    """
    Films list
    """
    url = config.infra.api.dsn + "/api/v1/films"
    body, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_number": 1, "page_size": 50, "sort": "-imdb_rating", "genre": STATIC_GENRE}, {"status": HTTPStatus.OK}),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films_genre(make_get_request, query_data, expected_answer):
    """
    Genre films
    """
    url = config.infra.api.dsn + "/api/v1/films"
    _, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_FILM_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_film_by_uuid(make_get_request, uuid, expected_status):
    """
    Specific film
    """
    url = config.infra.api.dsn + "/api/v1/films/" + uuid
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
async def test_film_not_found_by_uuid(make_get_request, uuid, expected_status):
    """
    Film not found
    """
    url = config.infra.api.dsn + "/api/v1/films/" + uuid
    _, _, status = await make_get_request(url)

    assert status == expected_status


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"query": STATIC_FILM_TITLE, "page_number": 1, "page_size": 50, "sort": "-imdb_rating"},
            {"status": HTTPStatus.OK, "length": 50},
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_from_cache(make_get_request, query_data, expected_answer):
    """
    Search from cache
    """
    url = config.infra.api.dsn + "/api/v1/films/search"
    body, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_FILM_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_film_by_uuid_from_cache(make_get_request, uuid, expected_status):
    """
    Film by uuid from cache
    """
    url = config.infra.api.dsn + "/api/v1/films/" + uuid
    body, _, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid
