from typing import Any

from elasticsearch import NotFoundError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi_service.src.core.logger import setup_logging

logger = setup_logging(logger_name=__name__)


class BaseError(Exception):
    """Base class for errors.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        body (Any): The response body associated with the error.
        errors (Tuple[Exception, ...]): A tuple of related exceptions.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        body: Any,
        errors: tuple[Exception, ...] | None = None,
    ):
        """
        Initialize the ServiceError.

        Args:
            message (str): The error message.
            status_code (int): The HTTP status code associated with the error.
            body (Any): The response body associated with the error.
            errors (Optional[Tuple[Exception, ...]]): A tuple of related exceptions.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body
        self.errors = errors if errors is not None else ()


class BadRequestError(BaseError):
    """Exception representing a 400 status code."""

    pass


class ElasticsearchConnectionError(ConnectionError):
    """Elasticsearch connection error."""

    pass


class RedisConnectionError(ConnectionError):
    """Redis connection error."""

    pass


async def not_found_exception_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    if isinstance(exc, NotFoundError):
        logger.warning(f"NotFoundError: {exc}")
        return JSONResponse(
            status_code=404,
            content={"message": "Item not found"},
        )

    raise exc


async def bad_request_exception_handler(request: Request, exc: BadRequestError) -> JSONResponse:
    if isinstance(exc, BadRequestError):
        logger.error(f"BadRequestError: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message, "body": exc.body, "errors": [str(error) for error in exc.errors]},
        )
    raise exc


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers for the application.

    Args:
        app (FastAPI): The FastAPI application.
    """
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(BadRequestError, bad_request_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
