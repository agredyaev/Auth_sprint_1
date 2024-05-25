import time

from redis import Redis

from tests.functional.settings import config

if __name__ == "__main__":
    redis_client = Redis(host=config.infra.redis.host, port=config.infra.redis.port)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
