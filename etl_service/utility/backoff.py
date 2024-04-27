import time
from functools import wraps
import random
from typing import Any, Callable, Tuple, Type

from etl_service.datastore_adapters.base_adapter import BaseAdapter
from etl_service.utility.logger import setup_logging
from etl_service.utility.settings import settings

logger = setup_logging()


def datastore_reconnect(func: Callable) -> Callable:
    """
    Decorator that reconnects to the datastore if it is lost.
    :param func: Function to decorate
    """

    @wraps(func)
    def wrapper(store: BaseAdapter, *args, **kwargs):
        if not store.is_connected:
            logger.warning(
                "Connection was lost: %r on call to %s, reconnecting",
                store,
                func.__name__,
            )
            store.reconnect()
        return func(store, *args, **kwargs)

    return wrapper


def get_backoff_delay(
    initial_delay: float = settings.general.backoff_initial_delay,
    factor: float = settings.general.backoff_factor,
    retries: int = 0,
    maximum: int = settings.general.backoff_max_delay,
) -> float:
    """
    Calculates backoff delay
    :param initial_delay: Initial backoff delay
    :param factor: Backoff factor
    :param retries: Number of retries
    :param maximum: Maximum backoff delay
    """
    delay = min(maximum, initial_delay * factor**retries)
    return random.uniform(0.1, delay + 1)


def backoff(retry_exceptions=Tuple[Type[Exception]] | Any) -> Any:
    """
    Backoff decorator.
    :param retry_exceptions: Exceptions to retry
    """

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except retry_exceptions as e:
                logger.exception(
                    "Retry exception %s is raised on call %s. Applying backoff ...",
                    e,
                    func.__name__,
                )
                attempt = 0
                delay = settings.general.backoff_initial_delay
                while True:
                    try:
                        return func(*args, **kwargs)
                    except retry_exceptions as e:
                        delay = get_backoff_delay(initial_delay=delay, retries=attempt)
                        logger.exception(
                            "Attempt No.%i on call %s with exception %s. next try in %s seconds",
                            attempt,
                            func.__name__,
                            e,
                            delay,
                        )
                        time.sleep(delay)
                        attempt += 1
            except Exception as e:
                logger.exception(
                    "Unexpected error on call %s: %s, Will not retry", e, func.__name__
                )
                raise

        return wrapper

    return decorator
