import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """
    orjson.dumps returns bytes, to match standard json.dumps we need to decode
    """
    return orjson.dumps(v, default=default).decode("utf8")


class IdMixin(BaseModel):
    """Mixin that adds a UUID primary key field to a model."""

    id: str


class NameMixin(BaseModel):
    """Mixin that adds a name field to a model."""

    name: str


class TitleMixin(BaseModel):
    title: str


class ORJSONMixin(BaseModel):
    """
    Mixin that adds ORJSON encoder/decoder to a model.
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        extra = "ignore"
