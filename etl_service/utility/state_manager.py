import json
from abc import ABC, abstractmethod
from typing import Any, Dict, NoReturn

from etl_service.datastore_adapters.redis_adapter import RedisAdapter
from etl_service.models.state import StateModel

class BaseStateManager(ABC):
    """Base class for state manager."""

    @abstractmethod
    def is_state_exists(self, key: str) -> bool | None:
        """Check if state exists in storage."""

    @abstractmethod
    def save_state(self, key: str, value: Any) -> NoReturn:
        """Save state to storage."""

    @abstractmethod
    def retrieve_state(self, key: str) -> Dict[str, Any] | None:
        """Retrieve state from storage."""


class RedisStateManager(BaseStateManager):
    """Redis state manager."""

    def __init__(self, redis_adapter: RedisAdapter):
        self.redis_adapter = redis_adapter

    def is_state_exists(self, key: str) -> int | None:
        return self.redis_adapter.exists(key)

    def save_state(self, key: str, value: Any) -> NoReturn:
        self.redis_adapter.set(key, json.dumps(value))

    def retrieve_state(self, key: str) -> Dict[str, Any] | None:
        result = self.redis_adapter.get(key)

        if result:
            result = json.loads(result)
        return result


class State:
    def __init__(self, storage: BaseStateManager, key: str):
        self.storage = storage
        self.key = key

    def exists(self):
        """Check if state exists in storage"""
        return self.storage.is_state_exists(self.key)

    def set(self, value: str) -> None:
        """Save state to storage"""
        self.storage.save_state(self.key, {"updated_at": value})

    def get(self) -> StateModel | None:
        """Retrieve state from storage"""
        result = self.storage.retrieve_state(self.key)

        if result:
            result = StateModel(**result)
        return result
