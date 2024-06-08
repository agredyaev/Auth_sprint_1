from typing import Any

import orjson
from async_fastapi_jwt_auth import AuthJWT  # type: ignore
from fastapi import HTTPException, status

from auth_service.src.interfaces.repositories import TokenRepositoryProtocol
from auth_service.src.interfaces.services import AuthJWTProtocol
from auth_service.src.schemas.request import (
    Token,
    TokenAccessToDenylist,
    TokenGet,
    TokenRefreshStore,
    TokenRefreshToDenylist,
    TokensCreate,
)
from auth_service.src.schemas.response import TokensResponse


class AuthJWTService(AuthJWTProtocol):
    """Implementation of AuthJWTProtocol"""

    def __init__(self, authjwt: AuthJWT, token_repository: TokenRepositoryProtocol):
        self.authjwt = authjwt
        self.token_repository = token_repository

    async def create_token(self, obj_in: TokensCreate) -> TokensResponse:
        model_json = obj_in.model_dump_json()
        access_token = await self.authjwt.create_access_token(subject=model_json, fresh=True)
        refresh_token = await self.authjwt.create_refresh_token(subject=model_json)
        refresh_jti = await self.authjwt.get_jti(refresh_token)
        await self.token_repository.set_token(TokenRefreshStore(name=refresh_jti))
        return TokensResponse(access_token=access_token, refresh_token=refresh_token)

    async def _is_not_valid(self, jti: str) -> bool:
        return await self.token_repository.is_in_denylist_or_not_exist(TokenGet(name=jti))

    async def _get_jtis(self, current_user: dict[str, Any]) -> list[str]:
        tokens = ["refresh_token", "access_token"]
        return [await self.authjwt.get_jti(current_user.get(token)) for token in tokens]

    async def _check_refresh_token(self) -> tuple[dict[str, Any], list[str]]:
        await self.authjwt.jwt_refresh_token_required()
        current_user = orjson.loads(await self.authjwt.get_jwt_subject())

        refresh_jti, access_jti = await self._get_jtis(current_user)

        if await self._is_not_valid(jti=refresh_jti):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid refresh token")

        return current_user, [refresh_jti, access_jti]

    async def _generate_new_tokens(self, current_user: dict[str, Any]) -> TokensResponse:
        current_user_json = orjson.dumps(current_user).decode("utf-8")
        new_access_token = await self.authjwt.create_access_token(subject=current_user_json, fresh=False)
        new_refresh_token = await self.authjwt.create_refresh_token(subject=current_user_json)
        new_refresh_jti = await self.authjwt.get_jti(new_refresh_token)
        await self.token_repository.set_token(TokenRefreshStore(name=new_refresh_jti))
        return TokensResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def _add_tokens_in_denylist(self, jtis: list[str]) -> None:
        for jti, schema in zip(jtis, [TokenRefreshToDenylist, TokenAccessToDenylist]):
            await self.revoke_token(schema(name=jti))

    async def refresh_token(self) -> TokensResponse:
        try:
            current_user, jtis = await self._check_refresh_token()
            await self._add_tokens_in_denylist(jtis=jtis)
            return await self._generate_new_tokens(current_user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
            ) from e

    async def revoke_token(self, obj_in: Token) -> None:
        try:
            if await self._is_not_valid(jti=obj_in.name):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Token is already revoked or not found"
                )
            await self.token_repository.set_token(obj_in)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not revoke token") from e
