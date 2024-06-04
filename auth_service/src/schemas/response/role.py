from auth_service.src.schemas.mixins import DescriptionMixin, IdMixin, NameMixin, ORMMixin


class RoleResponse(IdMixin, NameMixin, DescriptionMixin, ORMMixin):
    ...
