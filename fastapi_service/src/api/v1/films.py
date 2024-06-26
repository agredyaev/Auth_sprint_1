from enum import Enum
from http import HTTPStatus
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, Query, status

from fastapi_service.src.api.v1.models_response.film import DefaultFilmResponse, DetailedFilmResponse
from fastapi_service.src.api.v1.parameters.pagination import PaginationParameters, fetch_pagination_parameters
from fastapi_service.src.api.v1.transformers.film_transromer import DefaultFilmTransformer, DetailedFilmTransformer
from fastapi_service.src.core.exceptions import BadRequestError
from fastapi_service.src.services.film import FilmService, get_film_service

router = APIRouter(prefix="/films", tags=["films"])


class SortOrder(str, Enum):
    IMDB_RATING_ASC = "imdb_rating"
    IMDB_RATING_DESC = "-imdb_rating"


get_pagination_parameters = Depends(fetch_pagination_parameters)
get_film_service_dep = Depends(get_film_service)


@router.get(
    "",
    summary="Retrieve a list of films based on parameters",
    response_model=list[DefaultFilmResponse],
    status_code=status.HTTP_200_OK,
)
async def get_films(
    sort: list[SortOrder] = Query([SortOrder.IMDB_RATING_DESC]),
    genre: str | None = Query(None),
    pagination: PaginationParameters = get_pagination_parameters,
    film_service: FilmService = get_film_service_dep,
) -> list[DefaultFilmResponse]:
    """
    Retrieve a list of films based on sorting, genre, and pagination parameters.
    """
    try:
        films = await film_service.get_films(
            sort=[item.value for item in sort],
            genre=genre,
            page_number=pagination.page,
            page_size=pagination.size
        )
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    transformer = DefaultFilmTransformer()
    return transformer.to_response_list(films)


@router.get(
    "/search",
    summary="Full-text search for films",
    response_model=list[DefaultFilmResponse],
    status_code=status.HTTP_200_OK,
)
async def search_films(
    query: str,
    sort: list[SortOrder] = Query([SortOrder.IMDB_RATING_DESC]),
    pagination: PaginationParameters = get_pagination_parameters,
    film_service: FilmService = get_film_service_dep,
) -> list[DefaultFilmResponse]:
    """
    Perform a full-text search for films based on query, sorting, and pagination parameters.
    """
    try:
        films = await film_service.search_films(
            query=query,
            sort=[item.value for item in sort],
            page_number=pagination.page,
            page_size=pagination.size
        )
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    transformer = DefaultFilmTransformer()
    return transformer.to_response_list(films)


@router.get(
    "/{film_id}",
    summary="Retrieve detailed information about a film",
    response_model=DetailedFilmResponse,
    status_code=status.HTTP_200_OK,
)
async def get_film(film_id: str, film_service: FilmService = get_film_service_dep) -> DetailedFilmResponse:
    """
    Retrieve detailed information about a specific film by its ID.
    """
    try:
        film = await film_service.get_film_by_id(film_id)
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    if film is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")

    transformer = DetailedFilmTransformer()
    return transformer.to_response(film)
