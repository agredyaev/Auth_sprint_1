from auth_service.src.schemas.mixins import RoleIdMixin, UserIdMixin


class UserRoleAssign(UserIdMixin, RoleIdMixin): ...


class UserRoleRevoke(UserRoleAssign): ...
