"""Pydantic-based configuration system for Social Mimic Agent."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider Selection
    llm_provider: str = Field(default="gemini", validation_alias="LLM_PROVIDER")

    # API Keys
    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    huggingface_api_key: str = Field(default="", validation_alias="HUGGINGFACE_API_KEY")

    # Model Selection
    openai_model: str = Field(default="gpt-4o", validation_alias="OPENAI_MODEL")
    gemini_model: str = Field(default="gemini-1.5-flash", validation_alias="GEMINI_MODEL")
    huggingface_model: str = Field(default="", validation_alias="HUGGINGFACE_MODEL")

    # Simulation Settings
    default_memory_limit: int = Field(default=5, validation_alias="DEFAULT_MEMORY_LIMIT")
    max_agents: int = Field(default=10, validation_alias="MAX_AGENTS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
