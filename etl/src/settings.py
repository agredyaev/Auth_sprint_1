from dotenv import load_dotenv
from pydantic import SecretStr, BaseSettings, field_validator, Field, conint


class DatabaseSettings(BaseSettings):
    dbname: SecretStr
    user: SecretStr
    password: SecretStr
    host: str = "localhost"
    port: conint(ge=0, le=65535, strict=True) = 5432

    class Config:
        env_prefix = "DB_"

class ElasticSearchSettings(BaseSettings):
    host: SecretStr
    port: int = 9200

    class Config:
        env_prefix = "ES_"


class GeneralSettings(BaseSettings):
    batch_size: int = 100
    backoff_start: float = 0.1
    backoff_max: float = 10.0
    backoff_multiplier: float = 2.0

    class Config:
        env_prefix = "GEN_"


load_dotenv('.env', encoding='utf-8')

class Settings(BaseSettings):
    db: DatabaseSettings = Field(default=DatabaseSettings())
    elasticsearch: ElasticSearchSettings = Field(default=ElasticSearchSettings())
    general: GeneralSettings = Field(default=GeneralSettings())

    class Config:
        validate_all = True


class DatabaseSettings(BaseSettings):
    dbname: SecretStr
    user: SecretStr
    password: SecretStr
    host: SecretStr = "localhost"
    port: conint(ge=0, le=65535, strict=True) = 5432

    class Config:
        env_prefix = "DB_"


class ElasticSearchSettings(BaseSettings):
    host: SecretStr
    port: conint(ge=0, le=65535, strict=True) = 9200

    class Config:
        env_prefix = "ES_"


class GeneralSettings(BaseSettings):
    batch_size: int = 100
    backoff_start: float = 0.1
    backoff_max: float = 10.0
    backoff_multiplier: float = 2.0

    class Config:
        env_prefix = "GEN_"





settings = Settings()
