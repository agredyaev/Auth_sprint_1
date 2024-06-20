from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, status
from fastapi_limiter.depends import RateLimiter

from auth_service.src.interfaces.services import AuthJWTProtocol, UserAuthenticationProtocol, UserManagementProtocol
from auth_service.src.models import LoginHistory
from auth_service.src.schemas.pagination import (
    Page,
    PaginationParameters,
    get_pagination_params,
    paginate_records,
    sort_records,
)
from auth_service.src.schemas.request import (
    LoginRequest,
    UserCreate,
    UserPasswords,
    UserPasswordUpdate,
    UserRoleAssign,
    UserRoleRevoke,
    UserRoleVerify,
)
from auth_service.src.schemas.response import (
    LoginHistoryResponse,
    UserLoginResponse,
    UserLogoutResponse,
    UserPasswordUpdateResponse,
    UserRegistrationResponse,
    UserRoleAssignResponse,
    UserRoleRevokeResponse,
    UserRoleVerifyResponse,
    UserTokenRefreshResponse,
)
from auth_service.src.services import (
    get_token_management_service,
    get_user_authentication_service,
    get_user_management_service,
)
from auth_service.src.utils import check_if_token_in_denylist  # noqa
from auth_service.src.core.config import settings as config

router = APIRouter(prefix="/user", tags=["User"])

get_limiter = RateLimiter(times=config.api.limiter_times, seconds=config.api.limiter_seconds)


@router.post(
    "/signup",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
    description="User registration endpoint",
    dependencies=[Depends(get_limiter)],
)
async def signup_user(
    user: UserCreate,
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserRegistrationResponse:
    return await user_management_service.user_signup(user)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserLoginResponse,
    summary="User login",
    description="User login endpoint returns access and refresh tokens",
    dependencies=[Depends(get_limiter)],
)
async def login_user(
    user: LoginRequest,
    request: Request,
    user_authentication_service: Annotated[
        UserAuthenticationProtocol[Any, Any], Depends(get_user_authentication_service)
    ],
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserLoginResponse:
    verified_user = await user_management_service.check_password(user)
    permissions = await user_management_service.get_user_permissions(verified_user)
    await user_authentication_service.user_login(request=request, user=verified_user, permissions=permissions)
    return UserLoginResponse()


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=UserTokenRefreshResponse,
    summary="New access and refresh tokens",
    description="Get new access and refresh tokens",
    dependencies=[Depends(get_limiter)],
)
async def refresh_token(
    user_authentication_service: Annotated[
        UserAuthenticationProtocol[Any, Any], Depends(get_user_authentication_service)
    ],
) -> UserTokenRefreshResponse:
    await user_authentication_service.token_refresh()
    return UserTokenRefreshResponse()


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=UserLogoutResponse,
    summary="User logout",
    description="User logout endpoint",
    dependencies=[Depends(get_limiter)],
)
async def logout_user(
    user_authentication_service: Annotated[
        UserAuthenticationProtocol[Any, Any], Depends(get_user_authentication_service)
    ],
) -> UserLogoutResponse:
    await user_authentication_service.user_logout()
    return UserLogoutResponse()


@router.get(
    "/history",
    response_model=Page[LoginHistoryResponse],
    summary="User's login history",
    description="Get user's login history",
    dependencies=[Depends(get_limiter)],
)
async def login_history(
    user_authentication_service: Annotated[
        UserAuthenticationProtocol[Any, Any], Depends(get_user_authentication_service)
    ],
    pagination: Annotated[PaginationParameters, Depends(get_pagination_params)],
) -> Any:
    login_records: list[LoginHistory] = await user_authentication_service.login_history()
    sorted_records = sort_records(login_records, key="login_at")
    return paginate_records(sorted_records, page=pagination.page, page_size=pagination.page_size)


@router.post(
    "/password_update",
    response_model=UserPasswordUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="User password update",
    description="User password update endpoint",
    dependencies=[Depends(get_limiter)],
)
async def password_update(
    passwords: UserPasswords,
    token_management_service: Annotated[AuthJWTProtocol[Any, Any], Depends(get_token_management_service)],
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserPasswordUpdateResponse:
    current_user = await token_management_service.get_jwt_subject_json()
    return await user_management_service.update_password(
        UserPasswordUpdate(
            id=current_user.get("user_id"),
            data=passwords,
        )
    )


@router.post(
    "/role/assign",
    response_model=UserRoleAssignResponse,
    status_code=status.HTTP_200_OK,
    summary="User permissions assign",
    description="User permissions assign endpoint",
    dependencies=[Depends(get_limiter)],
)
async def assign_role(
    user_role: UserRoleAssign,
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserRoleAssignResponse:
    return await user_management_service.assign_role(user_role)


@router.post(
    "/role/revoke",
    response_model=UserRoleRevokeResponse,
    status_code=status.HTTP_200_OK,
    summary="User permissions revoke",
    description="User permissions revoke endpoint",
    dependencies=[Depends(get_limiter)],
)
async def revoke_role(
    user_role: UserRoleRevoke,
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserRoleAssignResponse:
    return await user_management_service.revoke_role(user_role)


@router.post(
    "/role/verify",
    response_model=UserRoleVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="User permissions verify",
    description="User permissions verify endpoint",
    dependencies=[Depends(get_limiter)],
)
async def verify_role(
    user_role: UserRoleVerify,
    user_management_service: Annotated[UserManagementProtocol[Any, Any], Depends(get_user_management_service)],
) -> UserRoleAssignResponse:
    return await user_management_service.verify_role(user_role)
