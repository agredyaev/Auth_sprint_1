from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from auth_service.src.core.default_user_roles import DefaultRole, DefaultRoles

__all__ = ["settings"]

from auth_service.src.utils.static_uuid import get_static_uuid

load_dotenv(find_dotenv())


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class RolesSettings(DefaultSettings):
    default: DefaultRole = DefaultRole(
        id=get_static_uuid(DefaultRoles.DEFAULT), name=DefaultRoles.DEFAULT, description="Default user role"
    )
    admin: DefaultRole = DefaultRole(
        id=get_static_uuid(DefaultRoles.ADMIN), name=DefaultRoles.ADMIN, description="Administrator role"
    )

    model_config = SettingsConfigDict(
        frozen=True,
    )


class AuthSuperuserSettings(DefaultSettings):
    username: str = Field(default="admin")
    password: str = Field(default="123")
    email: str = Field(default="admin@example.com")

    model_config = SettingsConfigDict(env_prefix="AUTH_SUPERUSER_")


class JWTSettings(DefaultSettings):
    authjwt_algorithm: str = "RS512"
    authjwt_public_key: str = Field(default_factory=lambda: (Path(__file__).parent / "keys" / "public.pem").read_text())
    authjwt_private_key: str = Field(
        default_factory=lambda: (Path(__file__).parent / "keys" / "private.pem").read_text()
    )
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set[str] = {"access", "refresh"}
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_token_expires: int = 60 * 15
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 7

    model_config = SettingsConfigDict(env_prefix="AUTH_JWT_")


class PostgresSettings(DefaultSettings):
    dsn: str = Field(default="")
    dsn_local: str = Field(default="")
    db_schema: str = Field(default="auth")
    echo_sql_queries: bool = Field(default=False)

    model_config = SettingsConfigDict(env_prefix="AUTH_POSTGRES_")


class RedisSettings(DefaultSettings):
    host: str = Field(default="redis")
    port: int = Field(default=6379)
    db_number: int = Field(default=0)
    dsn: RedisDsn = Field(default="redis://redis:6379/2")  # type: ignore
    namespace: str = Field(default="auth")

    model_config = SettingsConfigDict(env_prefix="AUTH_REDIS_")


class ApiSettings(DefaultSettings):
    default_page_number: int = 1
    default_page_size: int = 50
    prefix: str = Field(default="/api")
    version: str = Field(default="v1")


class GeneralSettings(DefaultSettings):
    log_level: str = Field(default="DEBUG")
    docs_url: str = Field(default="/api/openapi")
    openapi_url: str = Field(default="/api/openapi.json")
    version: str = Field(default="0.1.0")
    project_name: str = Field(default="Auth Service")
    project_folder: str = Field(default="auth_service")


class UvicornSettings(DefaultSettings):
    app: str = Field(default="auth_service.src.main:app")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9090)


class Settings(BaseSettings):
    pg: PostgresSettings = PostgresSettings()
    general: GeneralSettings = GeneralSettings()
    redis: RedisSettings = RedisSettings()
    api: ApiSettings = ApiSettings()
    uvicorn: UvicornSettings = UvicornSettings()
    jwt: JWTSettings = JWTSettings()
    su: AuthSuperuserSettings = AuthSuperuserSettings()
    rbac: RolesSettings = RolesSettings()

    model_config = SettingsConfigDict(validate_default=True)


settings = Settings()
