from fastapi import Query
from pydantic import BaseModel

from fastapi_service.src.core.config import settings


class PaginationParameters(BaseModel):
    page: int
    size: int


def fetch_pagination_parameters(
    page: int = Query(settings.api.default_page_number, gt=0, alias="page_number"),
    size: int = Query(settings.api.default_page_size, gt=0, alias="page_size"),
) -> PaginationParameters:
    return PaginationParameters(page=page, size=size)
