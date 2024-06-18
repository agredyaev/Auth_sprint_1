from auth_service.src.schemas.mixins import (
    DetailMixin,
    EmailMixin,
    IdMixin,
    ORMMixin,
    UserNameMixin,
)
from auth_service.src.schemas.response.role import RoleGetResponse


class UserResponse(IdMixin, UserNameMixin, EmailMixin, DetailMixin, ORMMixin):
    pass


class UserRegistrationResponse(UserResponse):
    detail: str = "User registered successfully"


class UserPasswordUpdateResponse(UserRegistrationResponse):
    detail: str = "Password updated successfully"


class UserLoginResponse(DetailMixin):
    detail: str = "Login successful"


class UserLogoutResponse(DetailMixin):
    detail: str = "Logout successful"


class UserTokenRefreshResponse(DetailMixin):
    detail: str = "Tokens refreshed successfully"


class UserRoleAssignResponse(IdMixin, DetailMixin):
    roles: list[RoleGetResponse]
    detail: str = "Roles assigned successfully"


class UserRoleRevokeResponse(IdMixin, DetailMixin):
    roles: list[RoleGetResponse]
    detail: str = "Roles revoked successfully"


class UserRoleVerifyResponse(IdMixin, DetailMixin):
    roles: list[RoleGetResponse]
    detail: str = "Roles verified successfully"
