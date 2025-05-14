from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT_DIR / ".env"
class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ENV_FILE_PATH

settings = Settings()
