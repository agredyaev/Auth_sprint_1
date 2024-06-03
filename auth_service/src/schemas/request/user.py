import datetime

from auth_service.src.schemas.mixins import FullNameMixin, IdMixin, LoginMixin, ORMMixin, PasswordMixin, UserIdMixin


class UserResponse(IdMixin, FullNameMixin, LoginMixin, ORMMixin):
    ...


class LoginHistory(IdMixin, UserIdMixin, LoginMixin, ORMMixin):
    user_agent: str
    login_time: datetime.datetime
