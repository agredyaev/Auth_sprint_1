import asyncio as ancio
from typing import Any

import pytest
import pytest_asyncio

from tests.fastapi_service.settings import config
from tests.fastapi_service.testdata.film import film_data
from tests.fastapi_service.utils.helpers import ElasticSearchHelper as ESIndex


@pytest.fixture(scope="module", name="films_data")
def films_data():
    bulk_query: list[dict[str, Any]] = []
    for row in film_data:
        data = {"_index": config.film.index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def film_index(es_client):
    return ESIndex(client=es_client, config=config.film)


@pytest_asyncio.fixture(scope="module", name="prepare_films_data")
async def prepare_films_data(film_index, films_data):
    await film_index.delete()
    await film_index.create()
    await film_index.update(films_data)
