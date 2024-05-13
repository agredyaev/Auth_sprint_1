import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field, RedisDsn, SecretStr
from pydantic_settings import BaseSettings

env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(env_path, encoding="utf-8")


class RedisSettings(BaseSettings):
    host: SecretStr = Field(...)
    port: int = Field(default=6379)
    db_number: int = Field(default=0)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    dsn: RedisDsn = Field(...)
    cache_expire_in_seconds: int = Field(default=(60 * 5))

    class Config:
        env_prefix = "REDIS_"


class ElasticSearchSettings(BaseSettings):
    host: SecretStr = Field(...)
    port: int = Field(default=9200)
    dsn: AnyHttpUrl = Field(default="http://localhost:9200")
    index: str = Field(...)

    class Config:
        env_prefix = "ELASTICSEARCH_"


class ApiSettings(BaseSettings):
    default_page_number: int = 1
    default_page_size: int = 50
    prefix: str = Field(default="/api")

    class Config:
        env_prefix = "API_"


class GeneralSettings(BaseSettings):
    log_level: str = Field(default="INFO")
    package_name: str = Field(...)
    docs_url: str = Field(default="/docs")
    openapi_url: str = Field(default="/openapi.json")
    version: str = Field(...)

    class Config:
        env_prefix = "GENERAL_"


class UvicornSettings(BaseSettings):
    app: str = Field(default="main:app")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    class Config:
        env_prefix = "UVICORN_"


class Settings(BaseSettings):
    eks: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    general: GeneralSettings = Field(default=GeneralSettings())
    redis: RedisSettings = Field(default=RedisSettings())
    api: ApiSettings = Field(default=ApiSettings())
    uvicorn: UvicornSettings = Field(default=UvicornSettings())

    class Config:
        validate_default = True


settings = Settings()
