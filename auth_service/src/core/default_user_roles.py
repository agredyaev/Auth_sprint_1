from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class DefaultRoles(str, Enum):
    """Default roles"""

    __slots__ = ()

    ADMIN = "admin"
    DEFAULT = "default"


class DefaultRole(BaseModel):
    id: UUID
    name: DefaultRoles
    description: str


class PermissionLevel(int, Enum):
    """Permission level"""

    __slots__ = ()

    NONE = 0
    READ = 5
    WRITE = 10
    ADMIN = 15


class DefaultPermission(BaseModel):
    id: UUID
    name: str
    level: PermissionLevel
    description: str
