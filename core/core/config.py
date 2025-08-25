# core/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()