from etl_service.datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from etl_service.models.movies import Filmwork
from etl_service.utility.logger import setup_logging
from etl_service.utility.state_manager import State
from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)

logger = setup_logging()


class FilmworkLoader(DataProcessInterface):
    def __init__(
        self,
        eks_conn: ElasticsearchAdapter,
        state: State,
        eks_index: str,
        batch_size: int,
    ):
        self.eks_conn = eks_conn
        self.state = state
        self.eks_index = eks_index
        self.batch_size = batch_size

    def process(self):
        """
        Load data from the database into the Elasticsearch index.
        Receives data from transformer.
        """

        saved_state = None

        try:
            while True:
                last_updated, data_in = yield
                data_in: list[Filmwork]
                logger.debug(f"Loader start:state data received: {last_updated}")

                if not saved_state:
                    saved_state = last_updated
                elif saved_state != last_updated:
                    logger.warning(
                        ",Loader: State is changed. Updating current state: `%s` with value: `%s`",
                        self.state.key,
                        saved_state,
                    )
                    self.state.set(str(saved_state))
                    saved_state = last_updated

                data = [
                    {
                        "_op_type": "update",
                        "_id": row.id,
                        "doc": {
                            "id": row.id,
                            "imdb_rating": row.rating,
                            "title": row.title,
                            "description": row.description,
                            "genres": row.genres_names,
                            "directors_names": row.directors_names,
                            "actors_names": row.actors_names,
                            "writers_names": row.writers_names,
                            "directors": [dict(director) for director in row.directors],
                            "actors": [dict(actor) for actor in row.actors],
                            "writers": [dict(writer) for writer in row.writers],
                        },
                        "doc_as_upsert": True,
                    }
                    for row in data_in
                ]

                self.eks_conn.chunked_bulk(
                    items=data,
                    batch_size=self.batch_size,
                    index=self.eks_index,
                    raise_on_exception=True,
                )

        except GeneratorExit:
            logger.debug("Loader: Load is finished: `%s`", self.state.key)
            if saved_state:
                logger.warning(
                    "Loader: Updating current state: `%s` with value: `%s`",
                    self.state.key,
                    saved_state,
                )
                self.state.set(str(saved_state))
                logger.debug("Loader end: state: `%s`", self.state.get())
