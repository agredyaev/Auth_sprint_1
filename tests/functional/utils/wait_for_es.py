import backoff

from elasticsearch import Elasticsearch, exceptions

from tests.functional.settings import config


@backoff.on_exception(backoff.expo, exceptions.ConnectionError, max_time=60)
def wait_for_es() -> None:
    if not es_client.ping():
        raise exceptions.ConnectionError("Elasticsearch is not available. Backoff...")


if __name__ == "__main__":
    es_client = Elasticsearch(hosts=config.infra.es.dsn)
    try:
        wait_for_es()
    finally:
        if es_client:
            es_client.transport.close()
