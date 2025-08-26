# core/core/config.py
from typing import Final
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "test"
    COOKIE_ACCESS_NAME: Final[str] = "access_token"
    COOKIE_REFRESH_NAME: Final[str] = "refresh_token"
    ACCESS_MAX_AGE: Final[int] = 5 * 60
    REFRESH_MAX_AGE: Final[int] = 7 * 24 * 3600

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
