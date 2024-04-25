import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import (
    AnyHttpUrl,
    Field,
    PostgresDsn,
    RedisDsn,
    SecretStr,
)

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(env_path, encoding="utf-8")


class RedisSettings(BaseSettings):
    host: SecretStr = Field(...)
    port: int = Field(default=6379)
    db_number: int = Field(default=0)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    dsn: RedisDsn = Field(...)

    class Config:
        env_prefix = "REDIS_"


class DatabaseSettings(BaseSettings):
    db: SecretStr = Field(...)
    user: SecretStr = Field(...)
    password: SecretStr = Field(...)
    host: SecretStr = Field(...)
    port: int = Field(default=5432)
    dsn: PostgresDsn = Field(...)
    extract_batch_size: int = Field(default=2000)

    class Config:
        env_prefix = "POSTGRES_"


class ElasticSearchSettings(BaseSettings):
    host: SecretStr = Field(...)
    port: int = Field(default=9200)
    dsn: AnyHttpUrl = Field(default="http://localhost:9200")
    index: str = Field(...)
    load_batch_size: int = Field(default=2000)

    class Config:
        env_prefix = "ELASTICSEARCH_"


class GeneralSettings(BaseSettings):
    backoff_start: float = 0.1
    backoff_max: float = 10.0
    backoff_multiplier: float = 2.0
    etl_timeout: int = 3
    retry_attempts: int = 3
    delay_seconds: int = 1

    class Config:
        env_prefix = "GENERAL_"


class Settings(BaseSettings):
    db: DatabaseSettings = Field(default=DatabaseSettings())
    eks: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    general: GeneralSettings = Field(default=GeneralSettings())
    redis: RedisSettings = Field(default=RedisSettings())

    class Config:
        validate_default = True


settings = Settings()