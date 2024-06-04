from pydantic import BaseModel, ConfigDict


class IdMixin(BaseModel):
    """Mixin that adds a UUID primary key field to a model."""

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


class PasswordMixin(BaseModel):
    """
    Mixin that adds a password field to a model.
    """

    password: str


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
