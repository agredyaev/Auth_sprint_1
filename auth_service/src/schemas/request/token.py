from typing import Sequence
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from auth_service.src.core.config import settings as conf
from auth_service.src.schemas.mixins import (
    NameMixin,
    RefreshTokenMixin,
    UserAgentMixin,
    UserIdMixin,
)


class Token(BaseModel):
    name: str = Field(default="token", description="jti")
    time: int = Field(default=0, description="exp")
    value: str = Field(default="false", description="is_in_denylist")

    @field_validator("name", mode="before")
    @staticmethod
    def set_name(v: str) -> str:
        return f"{conf.redis.namespace}:{v}"


class TokenRefreshStore(Token):
    time: int = conf.jwt.authjwt_refresh_token_expires


class TokenRefreshToDenylist(TokenRefreshStore):
    value: str = "true"


class TokenAccessToDenylist(Token):
    time: int = conf.jwt.authjwt_access_token_expires
    value: str = "true"


class TokenGet(NameMixin):
    pass


class TokensCreate(UserIdMixin):
    session_id: str | UUID
    permissions: Sequence[str]


class TokenRefreshData(RefreshTokenMixin, UserAgentMixin):
    pass


class TokenPair(BaseModel):
    access_token_cookie: str
    refresh_token_cookie: str


class TokenJTI(BaseModel):
    refresh_token_jti: TokenRefreshToDenylist
    access_token_jti: TokenAccessToDenylist
