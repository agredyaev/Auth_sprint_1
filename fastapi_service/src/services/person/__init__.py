from functools import lru_cache
from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from fastapi_service.src.db.elasticsearch import get_elastic
from fastapi_service.src.services.elasticsearch.client import ElasticsearchClient
from fastapi_service.src.services.elasticsearch.model_service import ModelService
from fastapi_service.src.services.elasticsearch.search_service import SearchService
from fastapi_service.src.services.person.service import PersonService


@lru_cache()
def get_person_service(
    elasticsearch_client: Annotated[AsyncElasticsearch, Depends(get_elastic)],
) -> PersonService:
    """
    Provider for FilmService.
    """
    elasticsearch_client_instance = ElasticsearchClient(elasticsearch_client)
    model_service = ModelService(elasticsearch_client_instance)
    search_service = SearchService(elasticsearch_client_instance)
    return PersonService(model_service=model_service, search_service=search_service)
