from pydantic import ValidationError

from person import Person
from settings import PersonSettings, set_env_vars


def load_personal_data() -> Person | None:
    try:
        personal_data = Person.parse_obj(PersonSettings())
    except ValidationError:
        return None
    else:
        return personal_data


def save_personal_data(person: Person) -> None:
    data = {f"MY_{key}": value for key, value in person.dict().items()}
    set_env_vars(data)
