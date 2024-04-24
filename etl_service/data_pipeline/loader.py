from etl_service.utility import backoff
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ElasticsearchException

class ElasticsearchLoader:
    def __init__(self, es_hosts, index_name):
        self.es = Elasticsearch(es_hosts)
        self.index_name = index_name

    @backoff.on_exception(backoff.expo,
                          ElasticsearchException,
                          max_tries=8,
                          max_time=300)
    def load_data(self, data):
        actions = [
            {
                "_index": self.index_name,
                "_id": doc.get("es_id"),
                "_source": doc,
            }
            for doc in data
        ]
        helpers.bulk(self.es, actions)
