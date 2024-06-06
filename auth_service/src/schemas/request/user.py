from auth_service.src.schemas.mixins import FullNameMixin, LoginMixin, PasswordMixin


class UserCreate(FullNameMixin, LoginMixin, PasswordMixin): ...


class UserUpdate(LoginMixin, PasswordMixin): ...
