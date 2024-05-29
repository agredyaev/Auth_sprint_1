from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import BulkIndexError, async_bulk

from tests.fastapi_service.settings import ElasticSearchSettings


class ElasticSearchHelper:
    def __init__(self, client: AsyncElasticsearch, config: ElasticSearchSettings):
        self.client = client
        self.index = config.index
        self.index_mapping = config.mapping

    async def check(self) -> None:
        await self.client.indices.stats(index=self.index, metric="indexing")

    async def create(self) -> None:
        await self.client.indices.create(index=self.index, **self.index_mapping)

    async def update(self, es_data: list[Any]) -> None:
        updated, errors = await async_bulk(client=self.client, actions=es_data, refresh="wait_for")
        if errors:
            if isinstance(errors, int):
                errors = [{"error": f"{errors} errors occurred"}]
            raise BulkIndexError("Errors during bulk update", errors)

    async def delete(self) -> None:
        if await self.client.indices.exists(index=self.index):
            await self.client.indices.delete(index=self.index)
