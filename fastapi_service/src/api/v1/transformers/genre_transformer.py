from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse, DetailedGenreResponse
from fastapi_service.src.api.v1.transformers.base_transformer import BaseTransformer
from fastapi_service.src.models.genre import Genre


class DefaultGenreTransformer(BaseTransformer):
    """
    Transforms a Genre object into a DefaultGenreResponse object
    """

    def to_response(self, genre: Genre) -> DefaultGenreResponse:
        return DefaultGenreResponse(uuid=genre.id, name=genre.name)


class DetailedGenreTransformer(BaseTransformer):
    """
    Transforms a Genre object into a DetailedGenreResponse object
    """

    def to_response(self, genre: Genre) -> DetailedGenreResponse:
        return DetailedGenreResponse(uuid=genre.id, name=genre.name)
