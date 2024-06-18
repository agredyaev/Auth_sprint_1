from typing import Any, Callable, Sequence

import orjson
from async_fastapi_jwt_auth import AuthJWT  # type: ignore
from async_fastapi_jwt_auth.exceptions import AuthJWTException  # type: ignore
from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth_service.src.core.config import settings as config
from auth_service.src.core.logger import setup_logging
from auth_service.src.db import get_session
from auth_service.src.models.permission import Permission
from auth_service.src.utils.db_operations import execute_list_query

logger = setup_logging(logger_name=__name__)


class PermissionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check user permissions before processing a request.

    This middleware intercepts incoming requests and checks if the user has the necessary
    permissions to access the requested endpoint. It uses JWT for authentication and authorization.

    Attributes:
        db_session (AsyncSession | None): The database session for querying permissions.
        authjwt (AuthJWT | None): The JWT authentication object.
        exempt_endpoints (list): List of endpoints that do not require permission checks.
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.db_session: AsyncSession | None = None
        self.authjwt: AuthJWT | None = None
        self.exempt_endpoints: list[str] = []
        logger.debug("Permission middleware initialized")

    async def load_exempt_endpoints(self) -> None:
        """
        Loads the list of endpoints that do not require permission checks.

        This method queries the database for permissions with a level of 0 and adds them
        to the exempt_endpoints list.
        """
        query = select(Permission).where(Permission.level == 0)
        permissions: Sequence[Permission] = await execute_list_query(self.db_session, query)  # type: ignore
        self.exempt_endpoints = [permission.name for permission in permissions]
        logger.debug(f"Exempt endpoints: {self.exempt_endpoints}")

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> JSONResponse:
        """
        Dispatches the request to the next middleware or endpoint after checking permissions.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or endpoint to call.

        Returns:
            JSONResponse: The HTTP response after processing the request.
        """
        logger.debug("Dispatching request")
        if not self.exempt_endpoints:
            await self.load_exempt_endpoints()

        path = request.url.path.split(config.api.version)[-1]
        logger.debug(f"Request path: {path}")
        if path not in self.exempt_endpoints:
            try:
                self.authjwt._request = request  # type: ignore
                await self.authjwt.jwt_required()  # type: ignore
                current_user = await self.authjwt.get_jwt_subject()  # type: ignore
                logger.debug(f"Current user: {current_user}")
                if not current_user:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials."}
                    )
                current_user_permissions = orjson.loads(current_user).get("permissions", [])

                if path not in current_user_permissions:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Insufficient rights."}
                    )

            except AuthJWTException as e:
                logger.error(f"AuthJWTException: {e}")
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": e.message},
                )

        response = await call_next(request)
        return response

    async def __call__(self, scope, receive, send):  # type: ignore
        if self.db_session is None:
            self.db_session = await get_session().__anext__()
        if self.authjwt is None:
            self.authjwt = AuthJWT()
        await super().__call__(scope, receive, send)
