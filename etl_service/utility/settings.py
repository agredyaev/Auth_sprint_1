from dotenv import load_dotenv
from pydantic import SecretStr, BaseSettings, field_validator, Field, conint, AnyHttpUrl, RedisDsn, PostgresDsn
import os

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path, encoding='utf-8')


class RedisSettings(BaseSettings):
    host: SecretStr
    port: conint(ge=0, le=65535, strict=True) = 6379
    db_number: conint(ge=0, le=65535, strict=True) = 0
    user: SecretStr
    password: SecretStr
    dsn: RedisDsn

    @field_validator('dsn')
    def assemble_redis_dsn(self, v: RedisDsn, values):
        if isinstance(v, RedisDsn):
            return v
        return RedisDsn.build(
            scheme='redis',
            user=values.get('user').get_secret_value(),
            password=values.get('password').get_secret_value(),
            host=values.get('host').get_secret_value(),
            port=str(values.get('port')),
            path=f"/{values.get('db_number')}"
        )

    class Config:
        env_prefix = "REDIS_"


class DatabaseSettings(BaseSettings):
    dbname: SecretStr
    user: SecretStr
    password: SecretStr
    host: SecretStr
    port: conint(ge=0, le=65535, strict=True) = 5432
    dsn: PostgresDsn
    extract_batch_size: conint(ge=0, le=100000, strict=True) = 2000

    @field_validator('dsn')
    def assemble_db_dsn(self, v: PostgresDsn, values):
        if isinstance(v, PostgresDsn):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('user').get_secret_value(),
            password=values.get('password').get_secret_value(),
            host=values.get('host').get_secret_value(),
            port=str(values.get('port')),
            path=f"/{values.get('dbname').get_secret_value()}"
        )

    class Config:
        env_prefix = "POSTGRES_"


class ElasticSearchSettings(BaseSettings):
    host: SecretStr
    port: conint(ge=0, le=65535, strict=True) = 9200
    dsn: AnyHttpUrl
    index: str
    load_batch_size: conint(ge=0, le=100000, strict=True) = 2000

    class Config:
        env_prefix = "ELASTICSEARCH_"


class GeneralSettings(BaseSettings):
    backoff_start: float = 0.1
    backoff_max: float = 10.0
    backoff_multiplier: float = 2.0

    class Config:
        env_prefix = "GENERAL_"


class Settings(BaseSettings):
    db: DatabaseSettings = Field(default=DatabaseSettings())
    eks: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    general: GeneralSettings = Field(default=GeneralSettings())
    redis: RedisSettings = Field(default=RedisSettings())

    class Config:
        validate_all = True


settings = Settings()
