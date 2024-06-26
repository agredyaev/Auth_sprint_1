import backoff
from redis import Redis, exceptions

from tests.auth_service.settings import config


@backoff.on_exception(backoff.expo, exceptions.ConnectionError, max_time=60, max_tries=50)
def wait_for_redis() -> None:
    if not redis_client.ping():
        raise exceptions.ConnectionError("Redis is not available. Backoff...")


if __name__ == "__main__":
    redis_client = Redis(host=config.infra.redis.host, port=config.infra.redis.port)
    try:
        wait_for_redis()
    finally:
        if redis_client:
            redis_client.close()
