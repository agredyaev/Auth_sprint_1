from pydantic import BaseModel


class UUIDMixin(BaseModel):
    uuid: str


class NameMixin(BaseModel):
    name: str


class TitleMixin(BaseModel):
    title: str
