from typing import Any, Optional, Tuple


class BaseServiceError(Exception):
    """Base class for service-related errors.

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
        errors: Optional[Tuple[Exception, ...]] = None,
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
        self.status_code = status_code
        self.body = body
        self.errors = errors if errors is not None else ()


class BadRequestError(BaseServiceError):
    """Exception representing a 400 status code."""
