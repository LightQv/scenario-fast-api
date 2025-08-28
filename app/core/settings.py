"""
Global settings from .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global settings from .env.
    """

    # App settings
    APP_NAME: str = "Scenario API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    # CORS settings
    FRONTEND_URL: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database settings
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES_IN: int

    # SMTP settings for email
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = True

    # Security settings
    PASSWORD_MIN_LENGTH: int = 7
    PASSWORD_MAX_LENGTH: int = 30
    USERNAME_MIN_LENGTH: int = 5
    USERNAME_MAX_LENGTH: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


# Instance globale des settings
settings = Settings()