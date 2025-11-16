"""Configuration management using Pydantic Settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None
    HERMES_API_KEY: Optional[str] = None
    NANO_BANANA_API_KEY: str
    VEO_API_KEY: str

    # AI Research Services
    TAVILY_API_KEY: str
    PERPLEXITY_API_KEY: Optional[str] = None
    EXA_API_KEY: Optional[str] = None

    # Research Configuration
    DEFAULT_RESEARCH_SERVICE: str = "tavily"
    DEEP_RESEARCH_MODE: bool = True

    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = "openai"
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000
    HERMES_API_URL: str = "https://inference-api.nousresearch.com"

    # Database
    DATABASE_URL: str = "sqlite:///./data/crypto_content.db"

    # File Storage
    DATA_DIR: str = "./data"
    PROJECTS_DIR: str = "./data/projects"
    CONTENT_DIR: str = "./data/content"

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
