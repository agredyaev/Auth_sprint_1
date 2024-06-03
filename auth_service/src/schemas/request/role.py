from auth_service.src.schemas.mixins import DescriptionMixin, IdMixin, NameMixin, ORMMixin, RoleIdMixin, UserIdMixin


class RoleCreate(NameMixin, DescriptionMixin):
    ...


class RoleResponse(IdMixin, NameMixin, DescriptionMixin, ORMMixin):
    ...


class RoleUpdate(NameMixin, DescriptionMixin):
    ...


class RoleAssign(UserIdMixin, RoleIdMixin):
    ...


class RoleRevoke(RoleAssign):
    ...


class RoleCheck(UserIdMixin):
    permission: str
