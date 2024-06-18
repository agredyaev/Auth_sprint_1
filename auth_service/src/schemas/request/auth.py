from auth_service.src.schemas.mixins import EmailMixin, PasswordMixin


class LoginRequest(EmailMixin, PasswordMixin):
    pass
