from typing import Any, Type, TypeVar, get_origin

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


def create_combinations(model_with_list: Any, combination_model: Type[ModelType]) -> list[dict[str, Any]]:
    """
    Create combinations from a model with a list field and another model for combinations.
    Automatically detects the list field in the model.
    :param model_with_list: Model instance with a list field
    :param combination_model: Model class for creating combinations
    :return: List of dictionaries representing combinations
    """

    list_field_name = None
    for field_name, field_type in model_with_list.__annotations__.items():
        if get_origin(field_type) is list:
            list_field_name = field_name
            break

    if list_field_name is None:
        raise ValueError("No list field found in the model")

    base_data = model_with_list.model_dump(exclude={list_field_name})
    list_data = getattr(model_with_list, list_field_name)

    combinations = []
    for item in list_data:
        combined_data = combination_model(**{**base_data, **item.model_dump()})
        combinations.append(combined_data.model_dump())

    return combinations
