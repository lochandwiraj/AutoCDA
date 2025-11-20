from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "AutoCDA"
    PROJECT_NAME: str = "AutoCDA"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str = "sqlite:///./autocda.db"

    # API keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Temporal.io
    TEMPORAL_HOST: str = "localhost:7233"
    TEMPORAL_NAMESPACE: str = "default"

    # Logging / Environment
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "CHANGE_ME_32CHAR"

    # API Config
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
