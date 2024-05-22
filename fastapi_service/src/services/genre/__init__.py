from functools import lru_cache
from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from fastapi_service.src.db.elasticsearch import get_elastic
from fastapi_service.src.services.elasticsearch.client import ElasticsearchClient
from fastapi_service.src.services.elasticsearch.model_service import ModelService
from fastapi_service.src.services.elasticsearch.search_service import SearchService
from fastapi_service.src.services.genre.service import GenreService


@lru_cache()
def get_genre_service(
    elasticsearch_client: Annotated[AsyncElasticsearch, Depends(get_elastic)],
) -> GenreService:
    """
    Provider for GenreService.
    """
    elasticsearch_client_instance = ElasticsearchClient(elasticsearch_client)
    model_service = ModelService(elasticsearch_client_instance)
    search_service = SearchService(elasticsearch_client_instance)
    return GenreService(model_service=model_service, search_service=search_service)
