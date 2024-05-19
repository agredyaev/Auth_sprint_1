from fastapi_service.src.api.v1.models_response.mixins import NameMixin, UUIDMixin


class DefaultGenreResponse(UUIDMixin, NameMixin): ...


class DetailedGenreResponse(DefaultGenreResponse): ...
