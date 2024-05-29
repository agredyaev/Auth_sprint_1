from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from tests.fastapi_service.testdata import es_mapping


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class ApiSettings(DefaultSettings):
    dsn: str = Field(default="http://nginx:80")
    health_check: str = Field(default="http://nginx:80/api/healthcheck")


class ElasticSearchSettings(DefaultSettings):
    dsn: str = Field(default="http://elasticsearch:9200")
    index: str = Field(default="movies")
    mapping: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)


class RedisSettings(DefaultSettings):
    host: str = Field("redis")
    port: int = Field(default=6379)

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class FilmSettings(ElasticSearchSettings):
    index: str = Field(default="movies")
    mapping: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)


class GenreSettings(ElasticSearchSettings):
    index: str = Field(default="genres")
    mapping: dict[str, Any] = Field(es_mapping.GENRES_MAPPING)


class PersonSettings(ElasticSearchSettings):
    index: str = Field(default="people")
    mapping: dict[str, Any] = Field(es_mapping.PERSONS_MAPPING)


class InfrastructureSettings(BaseSettings):
    api: ApiSettings = Field(default=ApiSettings())
    es: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    redis: RedisSettings = Field(default=RedisSettings())


class Settings(BaseSettings):
    infra: InfrastructureSettings = Field(default=InfrastructureSettings())
    film: FilmSettings = Field(default=FilmSettings())
    genre: GenreSettings = Field(default=GenreSettings())
    person: PersonSettings = Field(default=PersonSettings())


config = Settings()
