from typing import Any

from elasticsearch import AsyncElasticsearch


class ElasticsearchClientInterface:
    """
    Interface for Elasticsearch client.
    """

    async def get(self, index: str, id_: str) -> dict[str, Any]:
        """
        Get document by ID from the Elasticsearch index.
        """
        raise NotImplementedError

    async def search(
        self, index: str, query: dict[str, Any], sort: list[str], size: int, from_: int
    ) -> list[dict[str, Any]]:
        """
        Search documents in the Elasticsearch index.
        """
        raise NotImplementedError


class ElasticsearchClient(ElasticsearchClientInterface):
    """
    Elasticsearch client implementation.
    """

    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get(self, index: str, id_: str) -> dict[str, Any]:
        return await self._elastic.get(index=index, id=id_)

    async def search(
        self, index: str, query: dict[str, Any], sort: list[str], size: int, from_: int
    ) -> list[dict[str, Any]]:
        return await self._elastic.search(index=index, query=query, sort=sort, size=size, from_=from_)
