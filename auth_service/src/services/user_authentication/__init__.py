from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends

from auth_service.src.interfaces.repositories import (
    LoginHistoryRepositoryProtocol,
    TokenRepositoryProtocol,
)
from auth_service.src.interfaces.services import AuthJWTProtocol, UserAuthenticationProtocol
from auth_service.src.models import LoginHistory
from auth_service.src.repositories import get_login_history_repository, get_token_repository
from auth_service.src.services.token_management import get_token_management_service
from auth_service.src.services.user_authentication.service import UserAuthenticationService

__all__ = ["get_user_authentication_service"]


@lru_cache()
def get_user_authentication_service(
    authjwt: Annotated[AuthJWTProtocol[Any, Any], Depends(get_token_management_service)],
    token_repo: Annotated[TokenRepositoryProtocol[Any], Depends(get_token_repository)],
    login_history_repo: Annotated[LoginHistoryRepositoryProtocol[LoginHistory], Depends(get_login_history_repository)],
) -> UserAuthenticationProtocol[Any, Any]:
    """
    Provider for UserAuthenticationService
    """
    return UserAuthenticationService(authjwt=authjwt, token_repo=token_repo, login_history_repo=login_history_repo)
