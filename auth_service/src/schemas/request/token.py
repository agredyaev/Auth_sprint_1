from auth_service.src.schemas.mixins import AccessTokenMixin, RefreshTokenMixin


class Token(AccessTokenMixin, RefreshTokenMixin):
    token_type: str


class TokenRefreshRequest(RefreshTokenMixin):
    ...


class LogoutRequest(AccessTokenMixin):
    ...
