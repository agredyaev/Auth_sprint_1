import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from auth_service.src.utils import get_password_hash, get_timestamp
from auth_service.src.utils.date_format import format_datetime_with_timezone


class HashPasswordMixin(BaseModel):
    """
    Mixin that adds a password field to a model.
    Hashes the password before saving it to the database.
    """

    password: str = Field(...)

    @field_validator("password", mode="before")
    @staticmethod
    def hash_password(v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return get_password_hash(v)


class PasswordMixin(BaseModel):
    """
    Mixin that adds a password field to a model.
    """

    password: str


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


class LogoutMixin(BaseModel):
    """
    Mixin that adds a login field to a model.
    """

    logout_at: datetime.datetime = Field(default_factory=get_timestamp)


class IdMixin(BaseModel):
    """Mixin that adds a id field to a model."""

    id: UUID


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

    user_id: UUID


class RoleIdMixin(BaseModel):
    """
    Mixin that adds a role field to a model.
    """

    role_id: UUID


class DescriptionMixin(BaseModel):
    """
    Mixin that adds a description field to a model.
    """

    description: str | None = None


class FullNameMixin(BaseModel):
    """
    Mixin that adds a full name field to a model.
    """

    first_name: str | None = None
    last_name: str | None = None


class ORMMixin(BaseModel):
    """
    Mixin that add a ORM mode to a model.
    """

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={datetime.datetime: lambda v: format_datetime_with_timezone(v, 3)},
    )


class UserAgentMixin(BaseModel):
    """
    Mixin that adds a user agent field to a model.
    """

    user_agent: str


class UserNameMixin(BaseModel):
    """
    Mixin that adds a username field to a model.
    """

    username: str | None = Field(default=None, min_length=5, max_length=255)


class DetailMixin(BaseModel):
    """
    Mixin that adds a detail field to a model.
    """

    detail: str
