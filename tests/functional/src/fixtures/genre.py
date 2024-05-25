from typing import Any

import pytest
import pytest_asyncio

from tests.functional.settings import config
from tests.functional.testdata.genre import genre_data
from tests.functional.utils.helpers import ElasticSearchHelper as ESIndex


@pytest.fixture(scope="module", name="genres_data")
def genres_data():
    bulk_query: list[dict[str, Any]] = []
    for row in genre_data:
        data = {"_index": config.genre.index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def genre_index(es_client):
    return ESIndex(client=es_client, config=config.genre)


@pytest_asyncio.fixture(scope="module", name="prepare_genres_data")
async def prepare_genres_data(genre_index, genres_data):
    await genre_index.delete()
    await genre_index.create()
    await genre_index.update(genres_data)
