import datetime

from auth_service.src.schemas.mixins import FullNameMixin, IdMixin, LoginMixin, ORMMixin, PasswordMixin, UserIdMixin


class UserCreate(FullNameMixin, LoginMixin, PasswordMixin):
    ...


class UserResponse(IdMixin, FullNameMixin, LoginMixin, ORMMixin):
    ...


class UserUpdate(LoginMixin, PasswordMixin): ...


class LoginHistory(IdMixin, UserIdMixin, LoginMixin, ORMMixin):
    user_agent: str
    login_time: datetime.datetime
