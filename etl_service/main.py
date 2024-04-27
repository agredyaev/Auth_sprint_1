import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

from etl_service.data_pipeline.etl_processor import run_data_pipeline
from etl_service.data_pipeline.extractors.filmwork_extractor import FilmworkExtractor
from etl_service.data_pipeline.extractors.genre_extractor import GenreExtractor
from etl_service.data_pipeline.extractors.person_extractor import PersonExtractor
from etl_service.datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from etl_service.utility.logger import setup_logging
from etl_service.utility.settings import settings

logger = setup_logging()


def initialize_eks_index(eks_conn, index_name):
    """Ensure the Elasticsearch index exists and create it if it does not."""
    if not eks_conn.index_exists(index_name):
        logger.warning("Elasticsearch index %s is missing", index_name)
        with open("etl_service/index.json", "r") as f:
            index_configuration = json.load(f)
        eks_conn.index_create(index_name, body=index_configuration)
        logger.warning("Elasticsearch index %s created", index_name)


def main():
    with closing(ElasticsearchAdapter(settings.eks.dsn)) as eks_conn:
        initialize_eks_index(eks_conn, settings.eks.index)

    with ThreadPoolExecutor() as pool:
        pool.submit(run_data_pipeline, settings, GenreExtractor, "genre")
        pool.submit(run_data_pipeline, settings, PersonExtractor, "person")
        pool.submit(run_data_pipeline, settings, FilmworkExtractor, "filmwork")
        logger.critical("Processes started")


if __name__ == "__main__":
    main()
