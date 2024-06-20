from dotenv import find_dotenv, load_dotenv
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class AuthSuperuserSettings(DefaultSettings):
    username: str = Field(default="admin")
    password: str = Field(default="123")
    email: str = Field(default="admin@example.com")
    role_id: str = Field(default="8c6976e5-b541-0415-bde9-08bd4dee15df")

    model_config = SettingsConfigDict(env_prefix="AUTH_SUPERUSER_")


class ApiSettings(DefaultSettings):
    dsn: str = Field(default="http://nginx:80")
    health_check: str = Field(default="http://nginx:80/api/v1/healthcheck")
    api_path: str = Field(default="/api/v1")


class RedisSettings(DefaultSettings):
    host: str = Field("redis")
    port: int = Field(default=6379)
    db_number: int = Field(default=2)
    namespace: str = Field(default="auth")
    dsn: RedisDsn = Field(default="redis://redis:6379/2")  # type: ignore

    model_config = SettingsConfigDict(env_prefix="AUTH_REDIS")


class PostgresSettings(DefaultSettings):
    dsn: str = Field(default="")
    db_schema: str = Field(default="auth")
    echo_sql_queries: bool = Field(default=False)

    model_config = SettingsConfigDict(env_prefix="AUTH_POSTGRES_")


class InfrastructureSettings(BaseSettings):
    api: ApiSettings = Field(default=ApiSettings())
    pg: PostgresSettings = Field(default=PostgresSettings())
    redis: RedisSettings = Field(default=RedisSettings())


class Settings(BaseSettings):
    infra: InfrastructureSettings = Field(default=InfrastructureSettings())
    su: AuthSuperuserSettings = Field(default=AuthSuperuserSettings())


config = Settings()
