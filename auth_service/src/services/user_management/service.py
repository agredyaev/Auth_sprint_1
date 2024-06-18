from typing import Any, Sequence

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from auth_service.src.core.config import settings as cfg
from auth_service.src.interfaces.repositories import (
    RolePermissionRepositoryProtocol,
    UserRepositoryProtocol,
    UserRoleRepositoryProtocol,
)
from auth_service.src.interfaces.services import UserManagementProtocol
from auth_service.src.models import Permission, RolePermission, User, UserRole
from auth_service.src.schemas.mixins import RoleIdMixin
from auth_service.src.schemas.request import (
    LoginRequest,
    RoleGetPermissions,
    UserApplyNewPassword,
    UserCreate,
    UserGetByEmail,
    UserGetById,
    UserGetRolePermissions,
    UserPasswordUpdate,
    UserRoleAssign,
    UserRoleVerify,
)
from auth_service.src.schemas.response import (
    PermissionResponse,
    RoleGetResponse,
    UserPasswordUpdateResponse,
    UserRegistrationResponse,
    UserRoleAssignResponse,
    UserRoleRevokeResponse,
    UserRoleVerifyResponse,
)
from auth_service.src.utils import verify_password


class UserManagementService(UserManagementProtocol[Any, Any]):
    """Implementation of UserRegistrationProtocol"""

    def __init__(
        self,
        user_repo: UserRepositoryProtocol[User],
        user_role_repo: UserRoleRepositoryProtocol[UserRole],
        role_permission_repo: RolePermissionRepositoryProtocol[RolePermission],
    ):
        self.user_repo = user_repo
        self.user_role_repo = user_role_repo
        self.role_permission_repo = role_permission_repo

    async def user_signup(self, obj_in: UserCreate) -> UserRegistrationResponse:
        try:
            user = await self.user_repo.create_user(obj_in)
            await self.user_role_repo.create_records(
                UserRoleAssign(user_id=user.id, roles=[RoleIdMixin(role_id=cfg.rbac.default.id)])
            )
            return UserRegistrationResponse(
                id=user.id,
                username=user.username,
                email=user.email,
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"User with email {obj_in.email} already exists"
            ) from e

    async def check_password(self, obj_in: LoginRequest) -> User:
        user = await self.user_repo.get_user_by_email(user_data=UserGetByEmail(email=obj_in.email))
        if not user or not verify_password(obj_in.password, user.password):
            raise HTTPException(
                detail="Incorrect email or password.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return user

    async def update_password(self, user_data: UserPasswordUpdate) -> UserPasswordUpdateResponse:
        user = await self.user_repo.get_user_by_id(UserGetById(id=user_data.id))

        if not user or not verify_password(user_data.data.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect user or password")

        await self.user_repo.merge(UserApplyNewPassword(id=user.id, password=user_data.data.password))

        return UserPasswordUpdateResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )

    async def get_user_permissions(self, obj_in: User) -> list[str]:
        roles, _ = await self._get_user_role_response(
            UserGetRolePermissions(user_id=obj_in.id), self.user_role_repo.get_records
        )
        permissions = [permission.name for role in roles for permission in role.permissions]
        return permissions

    async def _get_user_role_response(self, model: Any, action: Any) -> tuple[list[RoleGetResponse], Any]:
        user_roles_list = await action(model)

        if not user_roles_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User roles not found")

        roles = []
        for user_role in user_roles_list:
            role_permissions: Sequence[Permission] = await self.role_permission_repo.get_permissions_list(
                RoleGetPermissions(role_id=user_role.role_id)
            )
            permissions = [
                PermissionResponse(id=permission.id, name=permission.name) for permission in role_permissions
            ]
            roles.append(RoleGetResponse(id=user_role.role_id, permissions=permissions))

        return roles, user_roles_list[0].user_id

    async def assign_role(self, obj_in: UserRoleAssign) -> UserRoleAssignResponse:
        try:
            roles, user_id = await self._get_user_role_response(obj_in, self.user_role_repo.create_records)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role already assigned to user")

        return UserRoleAssignResponse(id=user_id, roles=roles)

    async def revoke_role(self, obj_in: UserRoleAssign) -> UserRoleRevokeResponse:
        roles, user_id = await self._get_user_role_response(obj_in, self.user_role_repo.delete_records)

        return UserRoleRevokeResponse(id=user_id, roles=roles)

    async def verify_role(self, obj_in: UserRoleVerify) -> UserRoleVerifyResponse:
        roles, user_id = await self._get_user_role_response(obj_in, self.user_role_repo.check_records)

        return UserRoleVerifyResponse(id=user_id, roles=roles)
