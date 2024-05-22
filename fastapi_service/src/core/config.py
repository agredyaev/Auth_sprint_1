import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(env_path, encoding="utf-8")


class RedisSettings(BaseSettings):
    host: str = Field("redis")
    port: int = Field(default=6379)
    db_number: int = Field(default=0)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    dsn: RedisDsn = Field(...)
    cache_expiration: int = Field(default=(60 * 5))

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class ElasticSearchSettings(BaseSettings):
    host: SecretStr = Field(...)
    port: int = Field(default=9200)
    dsn: AnyHttpUrl = Field(default="http://elasticsearch:9200")
    films_index: str = Field(default="movies")
    genres_index: str = Field(default="genres")
    persons_index: str = Field(default="people")

    model_config = SettingsConfigDict(env_prefix="ELASTICSEARCH_")


class ApiSettings(BaseSettings):
    default_page_number: int = 1
    default_page_size: int = 50
    prefix: str = Field(default="/api")

    model_config = SettingsConfigDict(env_prefix="API_")


class GeneralSettings(BaseSettings):
    log_level: str = Field(default="DEBUG")
    package_name: str = Field(...)
    docs_url: str = Field(default="/api/openapi")
    openapi_url: str = Field(default="/api//openapi.json")
    version: str = Field(default="0.1.0")
    project_name: str = Field(default="FastAPI Movies")

    model_config = SettingsConfigDict(env_prefix="GENERAL_")


class UvicornSettings(BaseSettings):
    app: str = Field(default="fastapi_service.src.main:app")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9090)

    model_config = SettingsConfigDict(env_prefix="UVICORN_")


class Settings(BaseSettings):
    eks: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    general: GeneralSettings = Field(default=GeneralSettings())
    redis: RedisSettings = Field(default=RedisSettings())
    api: ApiSettings = Field(default=ApiSettings())
    uvicorn: UvicornSettings = Field(default=UvicornSettings())

    model_config = SettingsConfigDict(validate_default=True)


settings = Settings()
