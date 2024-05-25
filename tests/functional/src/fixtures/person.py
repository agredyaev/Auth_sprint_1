from typing import Any

import pytest
import pytest_asyncio

from tests.functional.settings import config
from tests.functional.testdata.person import person_data
from tests.functional.utils.helpers import ElasticSearchHelper as ESIndex


@pytest.fixture(scope="module", name="persons_data")
def persons_data():
    bulk_query: list[dict[str, Any]] = []
    for row in person_data:
        data = {"_index": config.person.index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def person_index(es_client):
    return ESIndex(client=es_client, config=config.person)


@pytest_asyncio.fixture(scope="module", name="prepare_persons_data")
async def prepare_persons_data(person_index, persons_data):
    await person_index.delete()
    await person_index.create()
    await person_index.update(persons_data)

