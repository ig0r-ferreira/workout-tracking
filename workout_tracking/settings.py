from pathlib import Path
from typing import Any

from models.person import Person

import dotenv
from pydantic import BaseSettings, HttpUrl, ValidationError


ENV_FILE_PATH = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"


class NutritionAPISettings(Settings):
    ENDPOINT: HttpUrl
    APP_ID: str
    APP_KEY: str

    class Config:
        env_prefix = "NLP_"


class SheetAPISettings(Settings):
    ENDPOINT: HttpUrl
    KEY_AUTH: str

    class Config:
        env_prefix = "SHEET_"


class PersonalDataSettings(Settings):
    gender: str
    weight_kg: float
    height_cm: float
    age: int

    class Config:
        case_sensitive = False
        env_prefix = "MY_"


def load_personal_data() -> Person | None:
    try:
        personal_data = Person.parse_obj(PersonalDataSettings())
    except ValidationError as err:
        return None
    else:
        return personal_data


def set_env_vars(variables: dict[str, Any]) -> None:
    for key, value in variables.items():
        dotenv.set_key(ENV_FILE_PATH, key.upper(), str(value))


def save_personal_data(person: Person) -> None:
    data = {f"MY_{key}": value for key, value in person.dict().items()}
    set_env_vars(data)

