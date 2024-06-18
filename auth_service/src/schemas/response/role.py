from auth_service.src.schemas.mixins import DescriptionMixin, DetailMixin, IdMixin, NameMixin, ORMMixin
from auth_service.src.utils.date_format import utc_plus3


class PermissionResponse(IdMixin, NameMixin, ORMMixin):
    pass


class RoleGetResponse(IdMixin, ORMMixin):
    permissions: list[PermissionResponse]


class RoleCreateResponse(RoleGetResponse, NameMixin, DescriptionMixin, DetailMixin):
    detail: str = "Role successfully created"


class RoleUpdateResponse(RoleCreateResponse):
    detail: str = "Role successfully updated"


class RoleDeleteResponse(IdMixin, ORMMixin, NameMixin, DescriptionMixin):
    detail: str = "Role successfully deleted"


class RoleListResponse(RoleGetResponse, NameMixin, DescriptionMixin, ORMMixin):
    created_at: utc_plus3
    updated_at: utc_plus3
