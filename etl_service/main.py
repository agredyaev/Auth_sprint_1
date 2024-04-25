import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

from utility.settings import settings
from utility.logger import setup_logging
from data_pipeline import etl_process
from data_pipeline.extractors.filmwork_extractor import FilmworkExtractor
from data_pipeline.extractors.genre_extractor import GenreExtractor
from data_pipeline.extractors.person_extractor import PersonExtractor

from datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter

logger = setup_logging()


def initialize_eks_index(eks_conn, index_name):
    """Ensure the Elasticsearch index exists and create it if it does not."""
    if not eks_conn.index_exists(index_name):
        logger.warning(f"EKS index `{index_name}` is missing")
        with open('etl_service/index.json', 'r') as f:
            index_configuration = json.load(f)
        eks_conn.index_create(index_name, body=index_configuration)
        logger.warning(f"EKS index `{index_name}` created")


def main():
    with closing(ElasticsearchAdapter(settings.eks.dsn)) as eks_conn:
        initialize_eks_index(eks_conn, settings.eks_index)

    with ThreadPoolExecutor() as pool:
        pool.submit(etl_process, settings, GenreExtractor, 'genre_data')
        pool.submit(etl_process, settings, PersonExtractor, 'person_data')
        pool.submit(etl_process, settings, FilmworkExtractor, 'film_work_data')
        logger.critical("Processes started")


if __name__ == '__main__':
    main()
