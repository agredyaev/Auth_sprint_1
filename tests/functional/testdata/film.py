import itertools
import random
from typing import Any

from faker import Faker
from faker.providers import DynamicProvider
from pydantic import BaseModel

from tests.functional.utils.base_entity import BaseEntity

STATIC_FILM_ID = "fcbcd7fe-5213-4917-b5f3-edc92716e076"
STATIC_FILM_TITLE = "Born best score."
STATIC_GENRE = "foreign"

people = {
    "actors": ["Melissa Harris", "Diane Anderson", "Joshua Jones"],
    "writers": ["Daniel Murphy", "Dawn Fox", "Tiffany Cooper"],
    "directors": ["Linda Myers", "Robert Shields", "Christine Brown"],
}

all_names = list(itertools.chain(*people.values()))

people_name_provider = DynamicProvider(
    provider_name="person_name",
    elements=all_names,
)

genres_names = ["foreign", "focus", "science", "game", "walk", "peace", "health", "ability"]

genres_name_provider = DynamicProvider(
    provider_name="genre_name",
    elements=genres_names,
)

fake = Faker()

fake.add_provider(people_name_provider)
fake.add_provider(genres_name_provider)


class FilmPerson(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float
    title: str
    description: str

    genres: list[FilmGenre]
    genres_names: list[str]

    directors: list[FilmPerson]
    directors_names: list[str]

    actors: list[FilmPerson]
    actors_names: list[str]

    writers: list[FilmPerson]
    writers_names: list[str]


class FilmEntity(BaseEntity):
    @property
    def model_attributes(self) -> dict[str, Any]:
        return {
            "imdb_rating": round(random.uniform(1, 10), 1),
            "title": STATIC_FILM_TITLE,
            "description": fake.paragraph(),
            "genres": self.create_uuids_and_names_list(genres_names, FilmGenre),
            "genres_names": random.sample(genres_names, k=3),
            "directors": self.create_uuids_and_names_list(people.get("directors"), FilmPerson),
            "directors_names": people.get("directors"),
            "actors": self.create_uuids_and_names_list(people.get("actors"), FilmPerson),
            "actors_names": people.get("actors"),
            "writers": self.create_uuids_and_names_list(people.get("writers"), FilmPerson),
            "writers_names": people.get("writers"),
        }


film_entity = FilmEntity(id_=STATIC_FILM_ID, num=60, fake=fake)
film_data = film_entity.generate_data(Film)
