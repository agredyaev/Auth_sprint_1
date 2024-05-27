from typing import Any, Protocol

from elasticsearch import AsyncElasticsearch


class ElasticsearchClientProtocol(Protocol):
    """
    Protocol for Elasticsearch client.
    """

    async def get(self, index: str, id_: str) -> dict[str, Any]:
        """
        Get document by ID from the Elasticsearch index.
        """
        ...

    async def search(
        self, index: str, query: dict[str, Any], sort: list[str], size: int, from_: int
    ) -> list[dict[str, Any]]:
        """
        Search documents in the Elasticsearch index.
        """
        ...


class ElasticsearchClient:
    """
    Elasticsearch client implementation.
    """

    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get(self, index: str, id_: str) -> dict[str, Any]:
        response = await self._elastic.get(index=index, id=id_)
        return response.body

    async def search(
        self, index: str, query: dict[str, Any], sort: list[str], size: int, from_: int
    ) -> list[dict[str, Any]]:
        response = await self._elastic.search(index=index, query=query, sort=sort, size=size, from_=from_)
        return [hit["_source"] for hit in response["hits"]["hits"] if "_source" in hit]
