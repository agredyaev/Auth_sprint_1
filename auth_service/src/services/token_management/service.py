from typing import Any

import orjson
from async_fastapi_jwt_auth import AuthJWT  # type: ignore
from fastapi import HTTPException, status

from auth_service.src.interfaces.services import AuthJWTProtocol
from auth_service.src.schemas.request import (
    TokenAccessToDenylist,
    TokenRefreshToDenylist,
)
from auth_service.src.schemas.request.token import TokenJTI
from auth_service.src.schemas.response import TokensResponse


class AuthJWTService(AuthJWTProtocol[Any, Any]):
    """Implementation of AuthJWTProtocol"""

    def __init__(self, authjwt: AuthJWT):
        self.authjwt = authjwt

    async def get_jwt_subject_json(self) -> Any | None:
        await self.authjwt.jwt_required()
        subject = await self.authjwt.get_jwt_subject()
        if not subject:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
        return orjson.loads(subject)

    async def get_tokens_jti(self) -> TokenJTI:
        await self.authjwt.jwt_required()
        raw_access_token = await self.authjwt.get_raw_jwt()
        await self.authjwt.jwt_refresh_token_required()
        raw_refresh_token = await self.authjwt.get_raw_jwt()

        if not raw_access_token or not raw_refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

        return TokenJTI(
            refresh_token_jti=TokenRefreshToDenylist(name=raw_refresh_token.get("jti")),
            access_token_jti=TokenAccessToDenylist(name=raw_access_token.get("jti")),
        )

    async def generate_tokens(self, current_user: Any, fresh: bool = True) -> TokensResponse:
        new_access_token = await self.authjwt.create_access_token(subject=current_user, fresh=fresh)
        new_refresh_token = await self.authjwt.create_refresh_token(subject=current_user)

        return TokensResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def set_cookies(self, obj_in: TokensResponse) -> None:
        await self.authjwt.set_access_cookies(obj_in.access_token)
        await self.authjwt.set_refresh_cookies(obj_in.refresh_token)

    async def unset_cookies(self) -> None:
        await self.authjwt.unset_jwt_cookies()

    async def extract_jti(self, encoded_token: str) -> str:
        print(await self.authjwt.get_raw_jwt(encoded_token))
        jti = await self.authjwt.get_jti(encoded_token)
        return jti
