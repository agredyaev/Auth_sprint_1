from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class JWTSettings(DefaultSettings):
    algorithm: str = Field("HS256")
    access_token_expiration: int = Field(default=300)
    refresh_token_expiration: int = Field(default=86400)
    public_key: SecretStr = Field(default="")
    private_key: SecretStr = Field(default="")

    model_config = SettingsConfigDict(env_prefix="AUTH_JWT_")


class PostgresSettings(DefaultSettings):
    host: str = Field("db")
    port: int = Field(default=5432)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    db: str = Field(...)
    dsn: str = Field(...)

    echo_sql_queries: bool = Field(default=False)

    model_config = SettingsConfigDict(env_prefix="AUTH_POSTGRES_")


class RedisSettings(DefaultSettings):
    host: str = Field("redis")
    port: int = Field(default=6379)
    db_number: int = Field(default=2)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    dsn: str = Field(...)
    namespace: str = Field(default="auth")

    model_config = SettingsConfigDict(env_prefix="AUTH_REDIS_")


class ApiSettings(DefaultSettings):
    default_page_number: int = 1
    default_page_size: int = 50
    prefix: str = Field(default="/api")


class GeneralSettings(DefaultSettings):
    log_level: str = Field(default="DEBUG")
    package_name: str = Field(...)
    docs_url: str = Field(default="/api/openapi")
    openapi_url: str = Field(default="/api/openapi.json")
    version: str = Field(default="0.1.0")
    project_name: str = Field(default="Auth Service")

    model_config = SettingsConfigDict(env_prefix="GENERAL_")


class UvicornSettings(DefaultSettings):
    app: str = Field(default="auth_service.src.main:app")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9090)


class Settings(BaseSettings):
    pg: PostgresSettings = Field(default=PostgresSettings())
    general: GeneralSettings = Field(default=GeneralSettings())
    redis: RedisSettings = Field(default=RedisSettings())
    api: ApiSettings = Field(default=ApiSettings())
    uvicorn: UvicornSettings = Field(default=UvicornSettings())
    jwt: JWTSettings = Field(default=JWTSettings())

    model_config = SettingsConfigDict(validate_default=True)


settings = Settings()
