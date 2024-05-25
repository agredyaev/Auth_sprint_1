import time

from elasticsearch import Elasticsearch

from tests.functional.settings import config

if __name__ == "__main__":
    es_client = Elasticsearch(hosts=config.infra.es.dsn)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
