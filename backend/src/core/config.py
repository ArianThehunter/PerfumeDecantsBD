"""
PerfumeDecantBD — Core Configuration
=====================================
Centralized settings using pydantic-settings for type-safe environment variable parsing.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_name: str = "PerfumeDecantBD"
    app_version: str = "1.0.0"
    environment: Literal["development", "staging", "production", "testing"] = "development"
    debug: bool = True
    log_level: str = "INFO"

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://perfume_admin:perfume_dev_2024@localhost:5432/perfumedecantbd"

    # ── Security ─────────────────────────────────────────────────────────────
    secret_key: str = "dev-secret-key-not-for-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # ── CORS ─────────────────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:5173,http://localhost:4173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # ── File Upload ──────────────────────────────────────────────────────────
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 10

    # ── Email (Placeholder) ──────────────────────────────────────────────────
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@perfumedecantbd.com"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
