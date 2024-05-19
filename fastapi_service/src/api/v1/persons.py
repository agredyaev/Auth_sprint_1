from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_service.src.services.exceptions import BadRequestError
from fastapi_service.src.services.person import PersonService, get_person_service
from fastapi_service.src.api.v1.parameters.pagination import PaginationParameters, fetch_pagination_parameters
from fastapi_service.src.api.v1.models_response.person import DefaultPersonResponse, DetailedPersonResponse, \
    DefaultFilmPersonResponse
from fastapi_service.src.api.v1.transformers.person_transformer import (DefaultPersonTransformer, \
                                                                        DetailedPersonTransformer,
                                                                        DefaultFilmPersonTransformer)

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get(
    "/search",
    summary="Full-text search for persons",
    response_model=list[DefaultPersonResponse],
    status_code=status.HTTP_200_OK,
)
async def search_person_by_query(
        query: str,
        pagination: PaginationParameters = Depends(fetch_pagination_parameters),
        person_service: PersonService = Depends(get_person_service),
) -> list[DefaultPersonResponse]:
    """
    Perform a full-text search for persons based on query and pagination parameters.

    :param query: The search query string.
    :param pagination: Pagination parameters including page number and page size.
    :param person_service: Dependency injection of PersonService.
    :return: List of DefaultPersonResponse objects.
    """
    try:
        persons = await person_service.search_persons(
            query=query, page_number=pagination.page, page_size=pagination.size
        )
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    transformer = DefaultPersonTransformer()
    return transformer.to_response_list(persons)


@router.get(
    "/{person_id}",
    summary="Retrieve detailed information about a person",
    response_model=DetailedPersonResponse,
    status_code=status.HTTP_200_OK,
)
async def get_person_info(
        person_id: str, person_service: PersonService = Depends(get_person_service)
) -> DetailedPersonResponse:
    """
    Retrieve detailed information about a specific person by their ID.

    :param person_id: The unique identifier of the person.
    :param person_service: Dependency injection of PersonService.
    :return: DetailedPersonResponse object containing detailed information about the person.
    """
    try:
        person = await person_service.get_person_by_id(person_id)
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    if person is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    transformer = DetailedPersonTransformer()
    return transformer.to_response(person)


@router.get(
    "/{person_id}/films",
    summary="Retrieve a list of films that a person participated in",
    response_model=list[DefaultFilmPersonResponse],
    status_code=status.HTTP_200_OK,
)
async def get_films_for_person(
        person_id: str,
        pagination: PaginationParameters = Depends(fetch_pagination_parameters),
        person_service: PersonService = Depends(get_person_service),
) -> list[DefaultFilmPersonResponse]:
    """
    Retrieve a list of films that a person participated in based on their ID.

    :param person_id: The unique identifier of the person.
    :param pagination: Pagination parameters including page number and page size.
    :param person_service: Dependency injection of PersonService.
    :return: List of DefaultFilmPersonResponse objects.
    """
    try:
        persons_with_films = await person_service.get_films_by_person_id(
            person_id=person_id,
            page_number=pagination.page,
            page_size=pagination.size
        )
    except BadRequestError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    transformer = DefaultFilmPersonTransformer()
    return transformer.to_response_list(persons_with_films)
