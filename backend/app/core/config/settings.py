from functools import lru_cache
from typing import Literal
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "My Fitness Buddy"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = False
    app_secret_key: str = Field(default="change-me")

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    api_v1_prefix: str = "/api/v1"

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "fitness_buddy"
    mysql_user: str = "fitness_user"
    mysql_password: str = "fitness_password"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    jwt_secret_key: str = Field(default="change-me-jwt-secret")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    cors_allow_localhost_regex: bool = True
    allow_admin_signup: bool = True

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@fitnessbuddy.local"

    @property
    def database_url(self) -> str:
        user = quote_plus(self.mysql_user)
        password = quote_plus(self.mysql_password)
        return (
            f"mysql+aiomysql://{user}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def cors_origin_regex(self) -> str | None:
        if self.is_development and self.cors_allow_localhost_regex:
            return r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
        return None

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
