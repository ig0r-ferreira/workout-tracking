from typing import Any, Protocol

import requests
from workout_tracking.settings import NutritionAPISettings


class NutritionAPI(Protocol):
    def get_exercises_from_text(
            self,
            text: str,
            gender: str = None,
            weight_kg: float = None,
            height_cm: float = None,
            age: int = None
    ) -> list[dict[str, Any]]:
        raise NotImplementedError()


class NutritionixAPI(NutritionAPISettings):
    def get_exercises_from_text(
            self,
            text: str,
            gender: str = None,
            weight_kg: float = None,
            height_cm: float = None,
            age: int = None
    ) -> list[dict[str, Any]]:
        response = requests.post(
            url=self.ENDPOINT,
            headers={
                "x-app-id": self.APP_ID,
                "x-app-key": self.APP_KEY,
                "Content-Type": "application/json"
            },
            json={
                "query": text,
                "gender": gender,
                "weight_kg": weight_kg,
                "height_cm": height_cm,
                "age": age
            }
        )
        data: dict | None = response.json()
        return (data or []) and data.get("exercises", [])
