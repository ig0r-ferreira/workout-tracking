from __future__ import annotations

from typing import Any

import requests.exceptions
from pydantic import BaseModel, Field, validator

from request_handler import Request
from settings import settings


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
        request = Request(
            method="POST",
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
        try:
            response = request.send()
        except requests.exceptions.RequestException as err:
            raise err
        else:
            data: dict | None = response.json()
            return (data or []) and data.get("exercises", [])


class Workout(BaseModel):
    date: str
    time: str
    exercise: Exercise

    @staticmethod
    def save_to_spreadsheet(workout: Workout):
        request = Request(
            method="POST",
            url=settings.SHEETY_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Authorization": settings.SHEETY_AUTH
            },
            json={
                "workout": {
                    **workout.dict(exclude={"exercise"}),
                    **workout.exercise.dict(by_alias=True)
                }
            }
        )
        try:
            request.send()
        except requests.exceptions.RequestException as err:
            raise err
