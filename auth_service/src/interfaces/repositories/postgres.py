from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.base import MergeRepositoryProtocol, RepositoryProtocol

T = TypeVar("T")


class PostgresRepositoryProtocol(RepositoryProtocol[T, Any, Any, Any], MergeRepositoryProtocol):
    pass
