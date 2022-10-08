from pathlib import Path
from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    TRACKER_ENDPOINT: HttpUrl = "https://trackapi.nutritionix.com/v2/" \
                                "natural/exercise"
    TRACKER_APP_ID: str
    TRACKER_APP_KEY: str
    SHEETY_ENDPOINT: HttpUrl
    SHEETY_AUTH: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
