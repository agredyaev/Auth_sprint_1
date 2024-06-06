import datetime

from auth_service.src.schemas.mixins import IdMixin, LoginMixin, ORMMixin, UserIdMixin


class LoginHistoryCreate(IdMixin, UserIdMixin, LoginMixin, ORMMixin):
    user_agent: str
    login_time: datetime.datetime
