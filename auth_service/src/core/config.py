from dotenv import find_dotenv, load_dotenv
from pydantic import Field, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class JWTSettings(DefaultSettings):
    public_key: SecretStr = Field(default="")
    private_key: SecretStr = Field(default="")
    authjwt_denylist_enabled: bool = Field(default=True)
    authjwt_denylist_token_checks: set[str] = Field(default={"access", "refresh"})
    authjwt_token_location: set[str] = Field(default={"cookies"})
    authjwt_cookie_csrf_protection: bool = Field(default=True)
    access_expires: int = Field(default=60 * 15)
    refresh_expires: int = Field(default=60 * 60 * 24 * 7)

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
    dsn: RedisDsn = Field(default="redis://localhost:6379")
    namespace: str = Field(default="auth")

    model_config = SettingsConfigDict(env_prefix="AUTH_REDIS_")


class ApiSettings(DefaultSettings):
    default_page_number: int = 1
    default_page_size: int = 50
    prefix: str = Field(default="/api")


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

    model_config = SettingsConfigDict(validate_default=True)


settings = Settings()
