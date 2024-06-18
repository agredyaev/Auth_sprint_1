from pydantic import BaseModel

from auth_service.src.schemas.mixins import AccessTokenMixin, RefreshTokenMixin


class TokensResponse(AccessTokenMixin, RefreshTokenMixin):
    token_type: str = "Bearer"


class TokenStatusResponse(BaseModel):
    status: str
    detail: str
