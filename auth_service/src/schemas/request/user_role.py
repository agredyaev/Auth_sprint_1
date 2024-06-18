from auth_service.src.schemas.mixins import EmailMixin, NameMixin, RoleIdMixin, UserIdMixin


class UserRoleCreate(UserIdMixin, RoleIdMixin):
    pass


class UserRoleDelete(UserRoleCreate):
    pass


class UserRoleAssign(UserIdMixin):
    roles: list[RoleIdMixin]


class UserRoleRevoke(UserRoleAssign):
    pass


class UserGetRolePermissions(UserIdMixin):
    pass


class UserRoleVerify(EmailMixin):
    role_names: list[NameMixin]
