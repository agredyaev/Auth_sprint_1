from fastapi_service.src.api.v1.models_response.mixins import UUIDMixin, TitleMixin


class DefaultPersonResponse(UUIDMixin):
    full_name: str


class DetailedPersonResponse(DefaultPersonResponse):
    ...


class DefaultFilmPersonResponse(UUIDMixin, TitleMixin):
    roles: list[str]
