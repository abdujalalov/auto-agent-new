"""Application settings and configuration management."""
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from app.core.config.constants import Environment


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    PROJECT_NAME: str = Field(
        default="AutoAgent",
        alias="PROJECT_NAME",
        description="Name of the project"
    )
    VERSION: str = Field(
        default="0.0.1",
        alias="VERSION",
        description="Version of the project"
    )
    API_V1_STR: str = Field(
        default="/api/v1",
        alias="API_V1_STR",
        description="Base path for API version 1"
    )
    ENVIRONMENT: str = Field(
        default=Environment.DEVELOPMENT,
        alias="APP_ENV",
        description="Application environment (e.g., development, production)"
    )

    LOG_DIR: Path = Field(
        default=Path("logs"),
        alias="LOG_DIR",
        description="Directory where application logs are stored"
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
        description="Logging level for the application (e.g., DEBUG, INFO, WARNING, ERROR)"
    )

    LOG_FORMAT: str = Field(
        default="json",  # Options: "json" or "console"
        alias="LOG_FORMAT",
        description="Format of the logs (json or console)"
    )


    LLM_MODEL_NAME: str = Field(
        default="openai:gpt-4o-mini",  # should include the provider prefix, e.g., "openai:gpt-4o-mini"
        alias="LLM_MODEL_NAME",
        description="Name of the LLM model to use"
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
settings = Settings()
