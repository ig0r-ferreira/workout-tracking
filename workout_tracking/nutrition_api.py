from typing import Any, Protocol

import requests

from settings import NutritionAPISettings


class NutritionAPI(Protocol):
    def get_exercises_from_text(
            self,
            text: str,
            personal_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        raise NotImplementedError()


class NutritionixAPI(NutritionAPISettings):
    def get_exercises_from_text(
            self,
            text: str,
            personal_data: dict[str, Any]
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
                **personal_data
            },
            timeout=10
        )
        data = response.json()
        return (data or []) and data.get("exercises", [])
