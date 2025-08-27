from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App settings
    app_name: str = "Scenario API"
    app_version: str = "2.0.0"
    app_port: int = 8000
    debug: bool = False

    # CORS settings
    frontend_url: str
    allowed_origins: list[str] = ["http://localhost:3000"]

    # Database settings
    database_url: str

    # JWT settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 43200  # 30 days

    # SMTP settings for email
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_use_tls: bool = True

    # Security settings
    password_min_length: int = 7
    password_max_length: int = 30
    username_min_length: int = 5
    username_max_length: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance globale des settings
settings = Settings()