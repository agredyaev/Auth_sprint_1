from typing import Any

from fastapi import HTTPException, Request, status

from auth_service.src.interfaces.repositories import (
    LoginHistoryRepositoryProtocol,
    TokenRepositoryProtocol,
)
from auth_service.src.interfaces.services import AuthJWTProtocol, UserAuthenticationProtocol
from auth_service.src.models import LoginHistory, User
from auth_service.src.schemas.request import (
    LoginHistoryCreate,
    LoginHistoryLogout,
    TokenRefreshStore,
    TokensCreate,
)
from auth_service.src.schemas.response import LoginHistoryResponse


class UserAuthenticationService(UserAuthenticationProtocol[Any, Any]):
    """
    Implementation of UserAuthenticationProtocol
    """

    def __init__(
        self,
        authjwt: AuthJWTProtocol[Any, Any],
        login_history_repo: LoginHistoryRepositoryProtocol[LoginHistory],
        token_repo: TokenRepositoryProtocol[Any],
    ):
        self.authjwt = authjwt
        self.token_repo = token_repo
        self.login_history_repo = login_history_repo

    async def user_login(self, request: Request, user: User, permissions: list[str]) -> None:
        user_agent = request.headers.get("User-Agent")
        user_agent = user_agent if user_agent else "Unknown"
        session = await self.login_history_repo.create_login_record(
            LoginHistoryCreate(user_id=user.id, user_agent=user_agent)
        )

        tokens = await self.authjwt.generate_tokens(
            current_user=TokensCreate(
                session_id=session.id, user_id=user.id, permissions=permissions
            ).model_dump_json(),
            fresh=True,
        )

        refresh_jti = await self.authjwt.extract_jti(encoded_token=tokens.refresh_token)
        await self.token_repo.set_token(TokenRefreshStore(name=refresh_jti))
        await self.authjwt.set_cookies(tokens)

    async def _add_tokens_to_denylist(self) -> None:
        jtis = await self.authjwt.get_tokens_jti()
        await self.token_repo.set_token(jtis.refresh_token_jti)
        await self.token_repo.set_token(jtis.access_token_jti)

    async def user_logout(self) -> None:
        current_user = await self.authjwt.get_jwt_subject_json()
        await self._add_tokens_to_denylist()
        await self.authjwt.unset_cookies()
        await self.login_history_repo.update_login_record(LoginHistoryLogout(id=current_user.get("session_id")))

    async def token_refresh(self) -> None:
        current_user_json = await self.authjwt.get_jwt_subject_json()
        current_user = TokensCreate(
            session_id=current_user_json.get("session_id"),
            user_id=current_user_json.get("user_id"),
            permissions=current_user_json.get("permissions"),
        ).model_dump_json()
        tokens = await self.authjwt.generate_tokens(current_user=current_user, fresh=False)
        await self._add_tokens_to_denylist()
        await self.authjwt.set_cookies(tokens)

    async def login_history(self) -> list[LoginHistoryResponse]:
        current_user = await self.authjwt.get_jwt_subject_json()
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user credentials")
        login_records = await self.login_history_repo.list_login_records(user_id)
        return [LoginHistoryResponse.model_validate(login_record) for login_record in login_records]
