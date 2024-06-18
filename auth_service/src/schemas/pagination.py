from typing import Generic, Sequence, TypeVar, cast

from fastapi.params import Query
from pydantic import BaseModel

from auth_service.src.core.config import settings as conf

T = TypeVar("T")


class PaginationParameters(BaseModel):
    page: int
    page_size: int


class Page(BaseModel, Generic[T]):
    response: list[T]
    page: int
    page_size: int
    total_pages: int
    total_items: int


def sort_records(records: Sequence[T], key: str, reverse: bool = True) -> list[T]:
    return sorted(records, key=lambda x: getattr(x, key), reverse=reverse)


def paginate_records(records: list[T], page: int, page_size: int) -> Page[T]:
    total_items = len(records)
    total_pages = (total_items + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    paginated_records = records[start:end]
    return Page(
        response=paginated_records, page=page, page_size=page_size, total_pages=total_pages, total_items=total_items
    )


def get_pagination_params(
    page: int = cast(int, Query(conf.api.default_page_number, ge=0, alias="page_number")),
    page_size: int = cast(int, Query(conf.api.default_page_size, ge=0, alias="page_size")),
) -> PaginationParameters:
    return PaginationParameters(page=page, page_size=page_size)
