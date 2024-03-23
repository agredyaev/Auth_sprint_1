import asyncio
from functools import wraps
from settings import settings
import logging


logger = logging.getLogger(__name__)

def backoff(start_sleep_time=None, factor=None, border_sleep_time=None):
    """
    Decorator that implements a retry mechanism with exponential backoff.

    This decorator will catch exceptions thrown by the decorated function and retry the function call,
    waiting an increasing amount of time between each retry, up to a maximum wait time. The wait time
    increases exponentially based on the number of attempts made. This is useful for operations that may
    fail temporarily due to external factors, such as network connectivity issues or rate limits.

    :param start_sleep_time: The initial wait time between retries in seconds
    :param factor: The factor by which the wait time increases after each retry
    :param border_sleep_time: The maximum wait time between retries in seconds.
    """

    start_sleep_time = start_sleep_time or settings.general.backoff_start
    factor = factor or settings.general.backoff_multiplier
    border_sleep_time = border_sleep_time or settings.general.backoff_max

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    t = min(border_sleep_time, start_sleep_time * (factor ** n))
                    logger.error(f"Error: {e}, retrying in {t} seconds...")
                    await asyncio.sleep(t)
                    n += 1

        return inner

    return func_wrapper
