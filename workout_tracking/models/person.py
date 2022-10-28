from pydantic import BaseModel, Field, validator


ACCEPTED_GENRES: dict[str, str] = {
    "m": "male",
    "male": "male",
    "f": "female",
    "female": "female"
}


class Person(BaseModel):
    gender: str
    weight_kg: float = Field(..., gt=0, le=600)
    height_cm: float = Field(..., gt=0, le=270)
    age: int = Field(..., gt=0, le=120)

    @validator("gender")
    def valid_gender(cls, value: str):
        gender = ACCEPTED_GENRES.get(value.lower())
        if gender is None:
            raise ValueError(f"{value!a} is not a valid option. ")

        return gender
