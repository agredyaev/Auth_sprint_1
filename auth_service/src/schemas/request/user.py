from uuid import UUID, uuid4

from pydantic import ConfigDict, Field

from auth_service.src.schemas.mixins import (
    EmailMixin,
    FullNameMixin,
    HashPasswordMixin,
    IdMixin,
    PasswordMixin,
    UserNameMixin,
    UUIDMixin,
)


class UserCreate(FullNameMixin, UserNameMixin, HashPasswordMixin, EmailMixin):
    pass


class UserGetById(UUIDMixin):
    pass


class UserGetByEmail(EmailMixin):
    pass


class UserPasswords(HashPasswordMixin):
    old_password: str


class UserPasswordUpdate(IdMixin):
    data: UserPasswords


class UserApplyNewPassword(IdMixin, PasswordMixin):
    pass


class AdminCreate(UserNameMixin, HashPasswordMixin, EmailMixin):
    id: UUID = Field(default_factory=uuid4)

    model_config = ConfigDict(
        frozen=True,
    )
