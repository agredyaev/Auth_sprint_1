from uuid import UUID

from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8)

    @field_validator("password", mode="before")
    def hash_password(cls, v: str) -> str:
        return pwd_context.hash(v)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)


class EmailMixin(BaseModel):
    """
    Mixin that adds an email field to a model.
    """

    email: EmailStr


class UUIDMixin(BaseModel):
    """
    Mixin that adds a id field to a model.
    """

    id: UUID


class IdMixin(BaseModel):
    """Mixin that adds a id field to a model."""

    id: str


class NameMixin(BaseModel):
    """Mixin that adds a name field to a model."""

    name: str


class RefreshTokenMixin(BaseModel):
    """
    Mixin that adds a refresh token field to a model.
    """

    refresh_token: str


class AccessTokenMixin(BaseModel):
    """
    Mixin that adds a access token field to a model.
    """

    access_token: str


class UserIdMixin(BaseModel):
    """
    Mixin that adds a user id field to a model.
    """

    user_id: str


class RoleIdMixin(BaseModel):
    """
    Mixin that adds a role field to a model.
    """

    role_id: str


class DescriptionMixin(BaseModel):
    """
    Mixin that adds a description field to a model.
    """

    description: str | None = None


class LoginMixin(BaseModel):
    """
    Mixin that adds a login field to a model.
    """

    login: str


class FullNameMixin(BaseModel):
    """
    Mixin that adds a full name field to a model.
    """

    first_name: str
    last_name: str


class ORMMixin(BaseModel):
    """
    Mixin that add a ORM mode to a model.
    """

    model_config = ConfigDict(from_attributes=True)


class UserAgentMixin(BaseModel):
    """
    Mixin that adds a user agent field to a model.
    """

    user_agent: str = Field(min_length=1, max_length=255)


class UserNameMixin(BaseModel):
    """
    Mixin that adds a username field to a model.
    """

    username: str = Field(min_length=1, max_length=255)
