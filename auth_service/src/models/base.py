from typing import Annotated, Any, Type

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

STR_512 = Annotated[str, 512]
STR_255 = Annotated[str, 255]
STR_50 = Annotated[str, 50]


class Base(DeclarativeBase):
    """Base model class"""

    type_annotations_map: dict[Type[Any], Any] = {
        STR_50: String(50),
        STR_255: String(255),
        STR_512: String(512),
    }

    def __repr__(self):
        class_attrs = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({class_attrs})"
