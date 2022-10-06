import requests
from settings import settings
from typing import Any


def extract_workout_data(description: str) -> dict[str, Any]:
    response = requests.post(
        url=settings.TRACKER_ENDPOINT,
        headers={
            "x-app-id": settings.TRACKER_APP_ID,
            "x-app-key": settings.TRACKER_APP_KEY
        },
        json={
            "query": description
        }
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    user_description = input("Tell me what exercises you did today: ").strip()
    print(extract_workout_data(user_description))


if __name__ == "__main__":
    main()
