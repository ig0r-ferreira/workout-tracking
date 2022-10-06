from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    TRACKER_ENDPOINT: str = "https://trackapi.nutritionix.com/v2/natural/" \
                            "exercise"
    TRACKER_APP_ID: str
    TRACKER_APP_KEY: str
    SHEETY_ENDPOINT: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
