"""
Core configuration settings for the accounting application.
"""
from typing import Any, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import secrets


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Modern Accounting System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Accounting System with comprehensive features"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    DEBUG: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./accounting.db"
    ECHO_SQL: bool = True

    # For production PostgreSQL
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: str = "5432"

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str) and v.startswith("sqlite"):
            return v
        if values.get("POSTGRES_SERVER"):
            return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
        return v

    # Google Gemini API (Primary AI Provider)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"  # Text generation
    GEMINI_VISION_MODEL: str = "gemini-pro-vision"  # Image/document processing
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048

    # OpenAI API (Optional Alternative)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.7

    # Anthropic API (Optional Alternative)
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    # Tesseract OCR
    TESSERACT_CMD: Optional[str] = None  # Path to tesseract executable

    # Redis (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {
        "pdf", "jpg", "jpeg", "png", "xlsx", "xls", "csv", "doc", "docx"
    }

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 1000

    # Currency
    DEFAULT_CURRENCY: str = "USD"

    # Date Format
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Localization
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: list[str] = ["en", "ar"]

    # Email (for sending invoices, etc.)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # AI Configuration
    AI_ENABLED: bool = True
    AI_AUTO_CATEGORIZE: bool = True
    AI_OCR_ENABLED: bool = True
    AI_PREDICTION_ENABLED: bool = True
    AI_CHAT_ENABLED: bool = True

    # Confidence Thresholds
    AI_CATEGORIZATION_THRESHOLD: float = 0.80
    AI_OCR_CONFIDENCE_THRESHOLD: float = 0.85
    AI_PREDICTION_CONFIDENCE_THRESHOLD: float = 0.75

    # Accounting Settings
    DECIMAL_PLACES: int = 4
    REQUIRE_APPROVAL_ABOVE: float = 10000.00
    AUTO_POST_INVOICES: bool = False
    AUTO_POST_BILLS: bool = False

    # Fiscal Year
    FISCAL_YEAR_START_MONTH: int = 1  # January

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
