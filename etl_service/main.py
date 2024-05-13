from concurrent.futures import ThreadPoolExecutor

from etl_service.data_pipeline.etl_processor import run_data_pipeline
from etl_service.data_pipeline.extractors.filmwork_extractor import FilmworkExtractor
from etl_service.data_pipeline.extractors.genre_extractor import GenreExtractor
from etl_service.data_pipeline.extractors.person_extractor import PersonExtractor
from etl_service.utility.logger import setup_logging
from etl_service.utility.settings import settings

logger = setup_logging()


if __name__ == "__main__":
    with ThreadPoolExecutor() as pool:
        logger.critical("Processes started")
        pool.submit(run_data_pipeline, settings, GenreExtractor, "genre")
        pool.submit(run_data_pipeline, settings, PersonExtractor, "person")
        pool.submit(run_data_pipeline, settings, FilmworkExtractor, "filmwork")
