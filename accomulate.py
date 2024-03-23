import time
from functools import wraps


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Декоратор для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора до граничного времени ожидания.

    :param start_sleep_time: начальное время ожидания в секундах.
    :param factor: коэффициент, на который увеличивается время ожидания при каждой следующей попытке.
    :param border_sleep_time: максимальное время ожидания между попытками.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0  # Счетчик попыток
            while True:
                try:
                    return func(*args, **kwargs)  # Попытка выполнить функцию
                except Exception as e:
                    # Расчет времени ожидания с учетом максимального значения
                    t = min(border_sleep_time, start_sleep_time * (factor**n))
                    print(f"Ошибка: {e}, повтор через {t} секунд...")
                    time.sleep(t)  # Ожидание перед следующей попыткой
                    n += 1  # Увеличение счетчика попыток

        return inner

    return func_wrapper


import abc
from typing import Any, Dict
from redis import Redis


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


import json
from typing import Dict, Any


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


import json
from redis import Redis
from typing import Dict, Any


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        """Инициализация с адаптером Redis."""
        self.redis_adapter = redis_adapter
        self.state_key = "app_state"  # Ключ для хранения состояния в Redis

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в Redis."""
        # Состояние сериализуется в JSON перед сохранением
        serialized_state = json.dumps(state)
        self.redis_adapter.set(self.state_key, serialized_state)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из Redis."""
        # Извлекаем состояние и десериализуем его из JSON
        serialized_state = self.redis_adapter.get(self.state_key)
        if serialized_state:
            return json.loads(serialized_state)
        else:
            # Возвращаем пустой словарь, если ничего не найдено
            return {}
