import abc
import json
from typing import Dict, Any


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""

class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str) -> None:
        """Инициализация с путем к файлу, где будет храниться состояние."""
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохраняет состояние в файл в формате JSON.

        :param state: Состояние для сохранения.
        """
        with open(self.file_path, "w") as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        """Извлекает состояние из файла. Если файл не существует, возвращает пустой словарь."""
        try:
            with open(self.file_path) as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Возвращает пустой словарь, если файл не найден


class State:
    def __init__(self, storage: BaseStorage) -> None:
        """Инициализация с хранилищем, откуда будут извлекаться и куда будут сохраняться данные."""
        self.storage = storage
        # Загрузка начального состояния из хранилища
        self._state = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Устанавливает значение для заданного ключа и сохраняет измененное состояние.

        :param key: Ключ, для которого устанавливается значение.
        :param value: Значение, которое нужно установить.
        """
        if value is None:
            self._state.pop(key, None)
        else:
            self._state[key] = value
        # Сохранение измененного состояния в хранилище
        self.storage.save_state(self._state)

    def get_state(self, key: str) -> Any:
        """Возвращает значение по заданному ключу. Если ключ не найден, возвращает None.

        :param key: Ключ, для которого запрашивается значение.
        """
        return self._state.get(key)