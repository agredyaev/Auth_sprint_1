from elasticsearch.connection import ConnectionPool
from contextlib import contextmanager
from elasticsearch import Elasticsearch
import psycopg2
from psycopg2.extras import RealDictCursor
from settings import settings
import logging
from backoff import backoff

logger = logging.getLogger(__name__)


class PostgresConnector:
    def __init__(self):
        self.dbname = settings.db.dbname
        self.user = settings.db.user
        self.password = settings.db.password
        self.host = settings.db.host
        self.port = settings.db.port

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                cursor_factory=RealDictCursor
            )
            yield conn
        except Exception as e:
            logger.error(f"PostgreSQL connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()


class ElasticsearchConnector:
    def __init__(self):
        self.host = settings.elasticsearch.host
        self.port = settings.elasticsearch.port
        self.connection_pool = ConnectionPool([{"host": self.host, "port": self.port}])
        self.es = Elasticsearch(connection_pool=self.connection_pool)

    @contextmanager
    def get_connection(self):
        try:
            yield self.es
            logger.info("Elasticsearch connection successful")
        except Exception as e:
            logger.error(f"Elasticsearch connection error: {e}")
            raise
        finally:
            self.es.transport.close()


@backoff()
def execute_postgres_query(query, parameters=None):
    """
    Executes a query against the PostgreSQL database with optional parameters.
    Utilizes the backoff mechanism for retries in case of failures.
    """
    connector = PostgresConnector()
    with connector.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()


@backoff()
def index_document_in_elasticsearch(index, doc_id, document):
    """
    Indexes a document in Elasticsearch under the specified index and document ID.
    Utilizes the backoff mechanism for retries in case of failures.
    """
    connector = ElasticsearchConnector()
    with connector.get_connection() as es:
        response = es.index(index=index, id=doc_id, document=document)
        return response
