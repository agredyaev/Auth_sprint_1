from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base model class"""
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
