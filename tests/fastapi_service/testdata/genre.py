from typing import Any

from faker import Faker
from faker.providers import DynamicProvider
from pydantic import BaseModel

from tests.fastapi_service.utils.base_entity import BaseEntity

STATIC_GENRE = "popular"
STATIC_GENRE_ID = "be0da6c2-fb3f-4ce3-9970-68078a5cf7ba"

genre_names = [
    "few",
    "science",
    "popular",
    "dog",
    "certainly",
    "believe",
    "agency",
    "behind",
    "crime",
    "firm",
    "through",
    "site",
    "movement",
    "tough",
    "real",
    "cut",
    "outside",
    "against",
    "baby",
    "turn",
    "majority",
    "hard",
    "relate",
    "be",
    "data",
    "market",
    "line",
    "indeed",
    "financial",
    "goal",
    "avoid",
    "attorney",
    "certain",
    "specific",
    "capital",
    "sell",
    "guy",
    "suffer",
    "pick",
    "opportunity",
    "continue",
    "official",
    "case",
    "call",
    "indicate",
    "even",
    "rather",
    "street",
    "economic",
]

genres_name_provider = DynamicProvider(
    provider_name="genre_name",
    elements=genre_names,
)

fake = Faker()

fake.add_provider(genres_name_provider)


class Genre(BaseModel):
    id: str
    name: str
    description: str


class GenreEntity(BaseEntity):
    @property
    def model_attributes(self) -> dict[str, Any]:
        return {
            "name": STATIC_GENRE,
            "description": fake.paragraph(),
        }

    def _create_entities_list(self, numi: int, model: type[BaseModel]) -> list[BaseModel]:
        return [model(id=str(self._fake.uuid4()), name=name, description=fake.paragraph()) for name in genre_names]

    def _get_entities_list(self, model: type[BaseModel]) -> list[BaseModel]:
        return self._create_entities_list(model=model, numi=0)


genre_entity = GenreEntity(id_=STATIC_GENRE_ID, fake=fake)
genre_data = genre_entity.generate_data(Genre)
