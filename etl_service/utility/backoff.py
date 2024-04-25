import time
from functools import wraps
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
            logger.warning("Connection was lost: %r on call to %s, reconnecting", store, func.__name__)
            store.reconnect()
            return func(store, *args, **kwargs)

    return wrapper


def backoff(
        backoff_start=settings.general.backoff_start,
        backoff_multiplier=settings.general.backoff_multipliere,
        backoff_max=settings.general.backoff_max,
        retry_exceptions=Tuple[Type[Exception]] | Any,
) -> Any:
    """
    Decorator that implements a retry mechanism with exponential backoff.

    :param backoff_start: The initial wait time between retries in seconds.
    :param backoff_multiplier: The factor by which the wait time increases after each retry.
    :param backoff_max: The maximum wait time between retries in seconds.
    :param retry_exceptions: Tuple of exception types that trigger a retry.
    """

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except retry_exceptions as e:
                logger.exception(
                    "Retry exception %s is raised on call %s. Applying backoff ...",
                    e, func.__name__
                )
                n = 0
                t = backoff_start
                while True:
                    try:
                        return func(*args, **kwargs)
                    except retry_exceptions as e:
                        if t == backoff_max:
                            break
                        t = min(backoff_max, t * (backoff_multiplier ** n))
                        logger.exception(
                            "Retry No.%i on call %s with exception %s. next try in %s seconds",
                            n, func.__name__, e, t
                        )
                        n += 1
                        time.sleep(t)
                    except Exception as e:
                        logger.exception(
                            "Fatal error: %s, on call %s. Will not retry.",
                            e, func.__name__
                        )
                        break

        return wrapper

    return decorator
