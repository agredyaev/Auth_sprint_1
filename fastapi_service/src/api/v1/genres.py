from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi_service.src.api.v1.transformers.genre_transformer import DefaultGenreTransformer
from fastapi_service.src.services.exceptions import BadRequestError
from fastapi_service.src.services.genre import GenreService, get_genre_service
from fastapi_service.src.api.v1.parameters.pagination import PaginationParameters, fetch_pagination_parameters
from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse, DetailedGenreResponse

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get(
    "",
    summary="Retrieve a list of genres",
    response_model=list[DefaultGenreResponse],
    status_code=status.HTTP_200_OK
)
async def get_genres(
        pagination: PaginationParameters = Depends(fetch_pagination_parameters),
        genre_service: GenreService = Depends(get_genre_service),
) -> list[DefaultGenreResponse]:
    """
    Retrieve a list of genres based on pagination parameters.

    :param pagination: Pagination parameters including page number and page size.
    :param genre_service: Dependency injection of GenreService.
    :return: List of DefaultGenreResponse objects.
    """
    try:
        genres = await genre_service.fetch_genres(page_number=pagination.page, page_size=pagination.size)
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    transformer = DefaultGenreTransformer()
    return transformer.to_response_list(genres)


@router.get(
    "/{genre_id}",
    summary="Retrieve detailed information about a genre",
    response_model=DetailedGenreResponse,
    status_code=status.HTTP_200_OK,
)
async def get_genre_info(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> DetailedGenreResponse:
    """
    Retrieve detailed information about a specific genre by its ID.

    :param genre_id: The unique identifier of the genre.
    :param genre_service: Dependency injection of GenreService.
    :return: DetailedGenreResponse object containing detailed information about the genre.
    """
    try:
        genre = await genre_service.get_genre_by_id(genre_id)
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    if genre is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    transformer = DetailedGenreResponse()
    return transformer.to_response(genre)
