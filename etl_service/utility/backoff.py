import time
from functools import wraps
from settings import settings
from logger import setup_logging
from typing import Callable, Type, Any, Tuple

from ..datastore_adapters import BaseAdapter


logger = setup_logging()


def datastore_reconnect(retry_attempts=3, delay_seconds=1):
    """
    Decorator to reconnect to client on failure with a specified number of retry attempts and a delay between attempts.

    :param retry_attempts: Number of times to retry the connection.
    :param delay_seconds: Delay in seconds between retry attempts.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(storage: BaseAdapter, *args, **kwargs):
            attempts = 0
            while attempts < retry_attempts:
                if not storage.is_connected:
                    logger.warning(f"Lost connection to client: `{storage}`. Attempting to establish new "
                                   f"connection... (Attempt {attempts+1}/{retry_attempts})")
                    try:
                        storage.reconnect()
                        return func(storage, *args, **kwargs)
                    except Exception as e:
                        logger.error(f"Error reconnecting to client: {e}. Retrying in {delay_seconds} seconds...")
                        attempts += 1
                        time.sleep(delay_seconds)
                    if attempts == retry_attempts:
                        logger.error("Max retry attempts reached. Failing operation.")
                        raise ConnectionError("Unable to reconnect to the client after several attempts.")
                else:
                    return func(storage, *args, **kwargs)
        return wrapper
    return decorator


def backoff(
        start_sleep_time=None,
        factor=None,
        border_sleep_time=None,
        retry_exceptions=Tuple[Type[Exception]]) -> Any:
    """
    Decorator that implements a retry mechanism with exponential backoff.

    :param start_sleep_time: The initial wait time between retries in seconds.
    :param factor: The factor by which the wait time increases after each retry.
    :param border_sleep_time: The maximum wait time between retries in seconds.
    :param retry_exceptions: Tuple of exception types that trigger a retry.
    """

    # Use provided settings or default to GeneralSettings
    start_sleep_time = start_sleep_time if start_sleep_time is not None else settings.backoff_start
    factor = factor if factor is not None else settings.backoff_multiplier
    border_sleep_time = border_sleep_time if border_sleep_time is not None else settings.backoff_max

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as e:
                    t = min(border_sleep_time, start_sleep_time * (factor ** n))
                    logger.error(
                        "Error: %s, on call %s. Will retrying in %s seconds",
                        e, func.__name__, t
                    )
                    time.sleep(t)
                    n += 1
                except Exception as e:
                    logger.error(
                        "Fatal error: %s, on call %s. Will not retry.",
                        e, func.__name__
                    )

        return wrapper

    return decorator
