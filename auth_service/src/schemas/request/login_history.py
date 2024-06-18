from auth_service.src.schemas.mixins import IdMixin, LogoutMixin, UserAgentMixin, UserIdMixin


class LoginHistoryCreate(UserIdMixin, UserAgentMixin):
    pass


class LoginHistoryLogout(IdMixin, LogoutMixin):
    pass
