from pydantic import BaseModel, Field, field_validator

from auth_service.src.core.config import settings as conf
from auth_service.src.schemas.mixins import AccessTokenMixin, RefreshTokenMixin, UserAgentMixin, UserNameMixin


class Token(BaseModel):
    name: str = Field(default="token", description="jti")
    time: int = Field(default=0, description="exp")
    value: str = Field(default="false", description="is_in_denylist")

    @field_validator("name", mode="before")
    def set_name(cls, v: str) -> str:
        return f"{conf.redis.namespace}:{v}"


class TokenRefreshStore(Token):
    time: int = conf.jwt.refresh_expires


class TokenRefreshToDenylist(TokenRefreshStore):
    value: str = "true"


class TokenAccessToDenylist(Token):
    time: int = conf.jwt.access_expires
    value: str = "true"


class TokenGet(Token):
    pass


class TokensCreate(UserNameMixin, UserAgentMixin):
    pass


class Login(UserNameMixin):
    username: str
    password: str


class Logout(AccessTokenMixin):
    pass


class TokenRefreshData(RefreshTokenMixin, UserAgentMixin):
    pass
