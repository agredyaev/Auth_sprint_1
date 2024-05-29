from http import HTTPStatus

import pytest
from faker import Faker

from tests.fastapi_service.settings import config
from tests.fastapi_service.testdata.person import (
    STATIC_PERSON_FULL_NAME,
    STATIC_PERSON_ID,
    STATIC_PERSON_NUMBER_OF_FILMS,
    person_data,
)

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer, expected_data",
    [
        (
            {
                "query": STATIC_PERSON_FULL_NAME,
            },
            {"status": HTTPStatus.OK, "length": 1},
            person_data,
        ),
        (
            {
                "query": "Unknown_Name",
            },
            {"status": HTTPStatus.OK, "length": 0},
            [],
        ),
        (
            {
                "query": STATIC_PERSON_FULL_NAME[:-1] + "x",
            },
            {"status": HTTPStatus.OK, "length": 1},
            person_data,
        ),
        (
            {
                "query": STATIC_PERSON_FULL_NAME.split(" ")[0],
            },
            {"status": HTTPStatus.OK, "length": 4},
            person_data,
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_persons_search(make_get_request, query_data, expected_answer, expected_data):
    """
    Persons search
    """
    url = config.infra.api.dsn + "/api/v1/persons/search"
    body, _, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    if expected_data:
        for person_response in body:
            person_id = person_response["uuid"]
            expected_person_list = [person for person in expected_data if person["id"] == person_id]
            assert (
                len(expected_person_list) == 1
            ), f"Person with ID {person_id} not found or multiple found in expected data."
            expected_person = expected_person_list[0]
            assert person_response["full_name"] == expected_person["full_name"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_PERSON_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_person_detail(make_get_request, uuid, expected_status):
    """
    Person detail
    """
    url = config.infra.api.dsn + "/api/v1/persons/" + uuid
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
@pytest.mark.usefixtures("prepare_persons_data")
async def test_person_not_found(make_get_request, uuid, expected_status):
    """
    Person not found
    """
    url = config.infra.api.dsn + "/api/v1/persons/" + uuid
    _, _, status = await make_get_request(url)

    assert status == expected_status


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (STATIC_PERSON_ID, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_persons_films(make_get_request, uuid, expected_status):
    """
    Person films
    """
    url = config.infra.api.dsn + f"/api/v1/persons/{uuid}/films"
    body, _, status = await make_get_request(url)

    assert status == expected_status
    assert len(body) == STATIC_PERSON_NUMBER_OF_FILMS
