from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter

from auth_service.src.interfaces.services import RoleManagementProtocol
from auth_service.src.schemas.pagination import (
    Page,
    PaginationParameters,
    get_pagination_params,
    paginate_records,
    sort_records,
)
from auth_service.src.schemas.request import (
    RoleDelete,
    RolePermissionCreate,
    RolePermissionUpdate,
)
from auth_service.src.schemas.response import (
    RoleCreateResponse,
)
from auth_service.src.schemas.response.role import RoleDeleteResponse, RoleListResponse, RoleUpdateResponse
from auth_service.src.services import (
    get_role_management_service,
)
from auth_service.src.utils import check_if_token_in_denylist  # noqa

router = APIRouter(prefix="/role", tags=["Role"])

get_limiter = RateLimiter(times=2, seconds=5)


@router.post(
    "/create",
    response_model=RoleCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Role creation",
    description="Role creation endpoint",
    dependencies=[Depends(get_limiter)],
)
async def create_role(
    role: RolePermissionCreate,
    role_management_service: Annotated[RoleManagementProtocol[Any, Any], Depends(get_role_management_service)],
) -> RoleCreateResponse:
    return await role_management_service.create_role(role)


@router.post(
    "/update",
    response_model=RoleUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Role update",
    description="Role update endpoint",
    dependencies=[Depends(get_limiter)],
)
async def update_role(
    role: RolePermissionUpdate,
    role_management_service: Annotated[RoleManagementProtocol[Any, Any], Depends(get_role_management_service)],
) -> RoleCreateResponse:
    return await role_management_service.update_role(role)


@router.post(
    "/delete",
    response_model=RoleDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Role deletion",
    description="Role deletion endpoint",
    dependencies=[Depends(get_limiter)],
)
async def delete_role(
    role: RoleDelete,
    role_management_service: Annotated[RoleManagementProtocol[Any, Any], Depends(get_role_management_service)],
) -> RoleCreateResponse:
    return await role_management_service.delete_role(role)


@router.get(
    "/list",
    response_model=Page[RoleListResponse],
    status_code=status.HTTP_200_OK,
    summary="Roles list",
    description="Roles list endpoint",
    dependencies=[Depends(get_limiter)],
)
async def list_roles(
    role_management_service: Annotated[RoleManagementProtocol[Any, Any], Depends(get_role_management_service)],
    pagination: Annotated[PaginationParameters, Depends(get_pagination_params)],
) -> Any:
    role_records: Sequence[RoleListResponse] = await role_management_service.list_roles()
    sorted_records = sort_records(role_records, key="updated_at")
    return paginate_records(sorted_records, page=pagination.page, page_size=pagination.page_size)
