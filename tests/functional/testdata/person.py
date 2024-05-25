import random
from enum import Enum
from typing import Any

from faker import Faker
from pydantic import BaseModel

from tests.functional.utils.base_entity import BaseEntity

fake = Faker()

STATIC_PERSON_ID = "b8bfc469-4dd0-49a9-bfbc-d706e3f67a84"
STATIC_PERSON_FULL_NAME = "David Hammond"
STATIC_PERSON_NUMBER_OF_FILMS = 5

person_names = [
    "Crystal Conway",
    "Deanna Jackson",
    "John Griffin",
    "Brittany Higgins",
    "Ryan Johnson",
    "Emily Duke",
    "Krystal Clark",
    "Rodney Gonzalez",
    "Andrew Lam",
    "Erika Allen",
    "Dr. Gloria Payne",
    "Andrew Clay",
    "Brandon Meyers",
    "Ms. Christy Silva",
    "Cheryl Cox",
    "Mackenzie Whitaker",
    "Jennifer Foster",
    "Peter Mccoy MD",
    "Kimberly Fitzgerald",
    "James Lloyd",
    "Monica Irwin",
    "Jessica Powers",
    "Miguel Smith DDS",
    "Richard Bell",
    "Kimberly Bell",
    "Sandra Anderson",
    "Melissa Case",
    "Elizabeth Hood",
    "Crystal Martin",
    "Destiny Roberts",
    "Abigail Watson MD",
    "Ashley Moore",
    "James Hanson",
    "Brandi Dickerson DVM",
    "Marcus Reyes",
    "Amy Vazquez",
    "Michael Kennedy",
    "Ryan Kramer",
    "Debra Jones",
    "Michael Kim",
    "Brittany Reyes",
    "Christopher Johnson",
    "Henry Silva",
    "Carol Reyes",
    "Lisa Clark",
    "Carla Gonzalez",
    "Kaitlyn Wall",
    "Jeffrey Johnson",
    "Holly Calderon",
    "Cheryl Gonzalez",
    "Mark Gutierrez",
    "Sylvia Gaines",
    "Carl Nixon",
    "Ian Barnes",
    "Samuel Jackson",
    "Kara Morgan",
    "Donna Perez",
    "Kevin Jones",
    "Alan Martinez",
    "April Brady",
    "Kevin Kerr",
    "Donald Good",
    "James Klein",
    "Michael Blackwell",
    "Sherry Fox",
    "Eric Dean",
    "Jennifer Anderson",
    "David Bryant",
    "Jasmin Williams",
    "Chelsea Lopez",
    "David Brown",
    "William Daniel",
    "Frank Pierce Jr.",
    "Victoria Erickson",
    "Dawn Freeman",
    "Scott Dixon",
    "Christopher Thompson",
    "Denise Newman",
    "Allison Zamora",
    "Terry Boone",
    "Patrick Hughes",
    "Tiffany Cook",
    "Michael Flores",
    "Elizabeth Brown",
    "Terri Welch",
    "Kimberly Hanson",
    "Danielle Martinez",
    "Mrs. Veronica Hicks",
    "Aaron Ellis",
    "Stephen Dalton",
    "Jackie Thompson",
    "Edward Hall",
    "Joseph Proctor",
    "Nathan Keith",
    "David Hansen",
    "Michael Johnson",
    "Peter Harper",
]


class PersonFilmRoles(str, Enum):
    DIRECTOR = "director"
    ACTOR = "actor"
    WRITER = "writer"


class PersonFilm(BaseModel):
    id: str
    title: str
    roles: list[PersonFilmRoles]
    imdb_rating: float


class Person(BaseModel):
    id: str
    full_name: str
    films: list[PersonFilm]


class PersonEntity(BaseEntity):
    @staticmethod
    def _create_movies_list(numi: int) -> list[PersonFilm]:
        return [
            PersonFilm(
                id=str(fake.uuid4()),
                title=fake.paragraph(),
                roles=random.choices(list(PersonFilmRoles), k=random.randint(1, 3)),
                imdb_rating=round(random.uniform(1, 10), 1),
            )
            for _ in range(numi)
        ]

    @property
    def model_attributes(self) -> dict[str, Any]:
        return {
            "full_name": STATIC_PERSON_FULL_NAME,
            "films": self._create_movies_list(STATIC_PERSON_NUMBER_OF_FILMS),
            "imdb_rating": round(random.uniform(1, 10), 1),
        }

    def _create_entities_list(self, numi: int, model: type[BaseModel]) -> list[BaseModel]:
        return [
            model(
                id=str(fake.uuid4()),
                full_name=name,
                films=self._create_movies_list(random.randint(1, 5)),
            )
            for name in person_names
        ]

    def _get_entities_list(self, model: type[BaseModel]) -> list[BaseModel]:
        return self._create_entities_list(model=model, numi=0)


person_entity = PersonEntity(id_=STATIC_PERSON_ID, fake=fake)
person_data = person_entity.generate_data(Person)
