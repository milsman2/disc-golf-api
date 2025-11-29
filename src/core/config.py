"""
Main configuration file for the API
"""

import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    """
    Parse CORS origins from environment variable
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Settings for API
    """

    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    API_PORT: int = 8000
    API_HOST: str = "localhost"  # Allow API_HOST from env
    API_BASE_URL: str | None = None
    ENVIRONMENT: Literal["local", "dev", "staging", "production"] = "local"
    FRONTEND_HOST: str = "http://localhost:3000"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Redis configuration
    REDIS_URL: str = "redis://localhost:6379"

    @computed_field
    @property
    def api_base_url(self) -> str:
        """
        Determine base API URL based on environment
        """
        if self.API_BASE_URL:
            return self.API_BASE_URL
        host = (
            self.API_HOST
            if hasattr(self, "API_HOST") and self.API_HOST
            else self.DOMAIN
        )
        if self.ENVIRONMENT in ["local", "dev"]:
            return f"http://{host}:{self.API_PORT}{self.API_V1_STR}"
        else:
            return f"https://{host}{self.API_V1_STR}"

    CORS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        """
        Combine CORS origins and front end
        """
        return [str(origin).rstrip("/") for origin in self.CORS] + [self.FRONTEND_HOST]

    PROJECT_NAME: str = "The Disc Golf API"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changethis"
    POSTGRES_OWNER: str = "postgres"
    POSTGRES_DB: str = "postgres"
    SQLITE_URI: str = "sqlite:///./test.db"
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field
    @property
    def sql_alchemy_db_uri(self) -> PostgresDsn | str | MultiHostUrl:
        """
        Set the database URI based on environment
        """
        if self.ENVIRONMENT == "local":
            return self.SQLITE_URI
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def sql_conn_args(self) -> dict[str, bool]:
        """
        Set the database connection arguments based on environment.
        Needed for SQLite in local development.
        """
        if self.ENVIRONMENT == "local":
            return {"check_same_thread": False}
        return {}

    @computed_field
    @property
    def engine_kwargs(self) -> dict[str, int]:
        """
        Set the database engine arguments based on environment.
        Needed for SQLite in local development.
        """
        if self.ENVIRONMENT == "local":
            return {}
        return {"pool_size": 10, "max_overflow": 20, "pool_timeout": 30}

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """
        Check if a secret is still set to the default value.
        """
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        Enforce not having a default secret as the value.
        """
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)

        return self

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=[".env"],
    )


settings = Settings.model_validate({})
