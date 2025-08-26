# core/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY : str = "test"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()