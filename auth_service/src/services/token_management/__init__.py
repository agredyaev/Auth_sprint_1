from functools import lru_cache
from typing import Annotated, Any

from async_fastapi_jwt_auth import AuthJWT  # type: ignore
from fastapi import Depends

from auth_service.src.interfaces.services import AuthJWTProtocol
from auth_service.src.services.token_management.service import AuthJWTService

__all__ = ["get_token_management_service", "AuthJWTProtocol"]


@lru_cache()
def get_token_management_service(
    authjwt: Annotated[AuthJWT, Depends()],
) -> AuthJWTProtocol[Any, Any]:
    """
    Provider for TokenManagementService
    """
    return AuthJWTService(authjwt=authjwt)
