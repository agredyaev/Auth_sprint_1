import asyncio
import logging
import os
import random
import uuid
from datetime import datetime
from typing import AsyncGenerator, AsyncIterable, List

import asyncpg
from dotenv import load_dotenv
from faker import Faker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

PG_DSN = os.getenv("POSTGRES_DSN")
logger.debug(f"Database connection string: {PG_DSN}")


class DatabasePopulator:
    """
    Populates database with fake data for testing purposes.

    :param db_dsn: Database connection string
    :type db_dsn: str
    """

    def __init__(self, db_dsn: str):
        self.db_dsn = db_dsn
        self.fake = Faker()
        self.conn_pool = None
        self.movies_count = 200000
        self.genres_count = 300
        self.pople_count = 1000

    async def connect(self):
        """Establish a database connection."""
        logger.info("Connecting to database...")
        self.conn_pool = await asyncpg.create_pool(dsn=self.db_dsn, max_size=20, min_size=10)
        logger.info("Database connection established.")

    async def close(self):
        """Close database connection."""
        logger.info("Closing database connection...")
        await self.conn_pool.close()
        logger.info("Database connection closed.")

    async def disable_indexes(self):
        """Disable indexes and constraints on the tables to speed up insertion."""
        logger.info("Disabling indexes and constraints...")
        async with self.conn_pool.acquire() as conn:
            await conn.execute("""
                ALTER TABLE content.genre DISABLE TRIGGER ALL;
                ALTER TABLE content.film_work DISABLE TRIGGER ALL;
                ALTER TABLE content.person DISABLE TRIGGER ALL;
                ALTER TABLE content.genre_film_work DISABLE TRIGGER ALL;
                ALTER TABLE content.person_film_work DISABLE TRIGGER ALL;
            """)

    async def enable_indexes(self):
        """Re-enable indexes and constraints after insertion."""
        logger.info("Re-enabling indexes and constraints...")
        async with self.conn_pool.acquire() as conn:
            await conn.execute("""
                ALTER TABLE content.genre ENABLE TRIGGER ALL;
                ALTER TABLE content.film_work ENABLE TRIGGER ALL;
                ALTER TABLE content.person ENABLE TRIGGER ALL;
                ALTER TABLE content.genre_film_work ENABLE TRIGGER ALL;
                ALTER TABLE content.person_film_work ENABLE TRIGGER ALL;
            """)

    async def copy_data(self, table: str, columns: List[str], data: AsyncIterable[tuple] | List[tuple]):
        """
        Uses the COPY command to bulk insert data into a specified table.

        :param table: Table name
        :type table: str
        :param columns: Columns to insert
        :type columns: list[str]
        :param data: Data to insert
        :type data: list[tuple]
        """
        logger.info(f"Inserting data into {table}...")
        try:
            async with self.conn_pool.acquire() as conn:
                await conn.copy_records_to_table(table_name=table, records=data, columns=columns, schema_name="content")
        except Exception as e:
            logger.error(f"Failed to insert data into {table}: {e}")
        logger.info(f"Data inserted into {table}.")

    async def async_gen(self, num: int, *args) -> AsyncGenerator[tuple, None]:
        """
        Asynchronously generates data tuples based on provided callables.

        :param num: Number of tuples to generate
        :type num: int
        :param args: Callables that generate tuple elements
        :type args: list[callable]
        :yield: Generated data tuples
        :rtype: AsyncGenerator[tuple, None]
        """
        for _ in range(num):
            yield tuple(arg() if callable(arg) else arg for arg in args)

    async def insert_genres(self):
        await self.copy_data(
            "genre",
            ["created_at", "updated_at", "id", "name"],
            self.async_gen(
                self.genres_count,
                lambda: datetime.now(),
                lambda: datetime.now(),
                lambda: str(uuid.uuid4()),
                lambda: self.fake.word(),
            ),
        )

    async def insert_movies(self):
        await self.copy_data(
            "film_work",
            ["created_at", "updated_at", "id", "title", "description", "creation_date", "rating", "type"],
            self.async_gen(
                self.movies_count,
                lambda: datetime.now(),
                lambda: datetime.now(),
                lambda: str(uuid.uuid4()),
                lambda: self.fake.sentence(nb_words=5),
                lambda: self.fake.text(),
                lambda: self.fake.date_this_century(),
                lambda: round(random.uniform(1, 10), 2),
                lambda: random.choice(["movie", "tv_show"]),
            ),
        )

    async def insert_people(self):
        await self.copy_data(
            "person",
            ["created_at", "updated_at", "id", "full_name"],
            self.async_gen(
                self.pople_count,
                lambda: datetime.now(),
                lambda: datetime.now(),
                lambda: str(uuid.uuid4()),
                lambda: self.fake.name(),
            ),
        )

    async def insert_genre_film_work(self, genres, movies):
        genre_film_works = [
            (str(uuid.uuid4()), datetime.now(), random.choice(genres)["id"], movie["id"]) for movie in movies
        ]
        await self.copy_data("genre_film_work", ["id", "created_at", "genre_id", "film_work_id"], genre_film_works)

    async def insert_person_film_work(self, people, movies):
        person_film_works = [
            (
                str(uuid.uuid4()),
                random.choice(people)["id"],
                datetime.now(),
                movie["id"],
                random.choice(["actor", "director", "writer"]),
            )
            for movie in movies
        ]
        await self.copy_data(
            "person_film_work", ["id", "person_id", "created_at", "film_work_id", "role"], person_film_works
        )

    async def is_populated(self) -> bool:
        async with self.conn_pool.acquire() as conn:
            genres = await conn.fetch("SELECT count(*) as count FROM content.genre")
            movies = await conn.fetch("SELECT count(*) as count FROM content.film_work")
            people = await conn.fetch("SELECT count(*) as count FROM content.person")

            return all(
                [
                    genres[0]["count"] >= self.genres_count,
                    movies[0]["count"] >= self.movies_count,
                    people[0]["count"] >= self.pople_count,
                ]
            )
    async def populate(self):
        await self.disable_indexes()
        await asyncio.gather(
            self.insert_genres(),
            self.insert_movies(),
            self.insert_people(),
        )

        async with self.conn_pool.acquire() as conn:
            genres = await conn.fetch("SELECT id FROM content.genre")
            movies = await conn.fetch("SELECT id FROM content.film_work")
            people = await conn.fetch("SELECT id FROM content.person")

        await asyncio.gather(self.insert_genre_film_work(genres, movies), self.insert_person_film_work(people, movies))

        await self.enable_indexes()
        await self.close()


async def main():
    processor = DatabasePopulator(db_dsn=PG_DSN)
    await processor.connect()
    if_populated = await processor.is_populated()
    if not if_populated:
        logger.info("Populating DB")
        await processor.populate()
    else:
        logger.info("DB is already populated")
    await processor.close()

if __name__ == "__main__":
    asyncio.run(main())
