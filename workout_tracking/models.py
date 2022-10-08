from __future__ import annotations

import requests
from pydantic import BaseModel, Field, validator
from settings import settings
from typing import Any


class Exercise(BaseModel):
    name: str = Field(..., alias="exercise")
    duration_min: float = Field(..., alias="duration")
    nf_calories: float = Field(..., alias="calories")

    class Config:
        allow_population_by_field_name = True

    @validator("name", pre=True, always=True)
    def set_name_to_title(cls, value: str) -> str:
        return value.title()

    @staticmethod
    def extract_data_from_text(text: str) -> list[dict[str, Any]]:
        response = requests.post(
            url=settings.TRACKER_ENDPOINT,
            headers={
                "x-app-id": settings.TRACKER_APP_ID,
                "x-app-key": settings.TRACKER_APP_KEY,
                "Content-Type": "application/json"
            },
            json={
                "query": text
            }
        )
        response.raise_for_status()
        return response.json().get("exercises", [])


class Workout(BaseModel):
    date: str
    time: str
    exercise: Exercise

    @staticmethod
    def save_to_spreadsheet(workout: Workout):
        response = requests.post(
            url=settings.SHEETY_ENDPOINT,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "workout": {
                    **workout.dict(exclude={"exercise"}),
                    **workout.exercise.dict(by_alias=True)
                }
            }
        )
        response.raise_for_status()
