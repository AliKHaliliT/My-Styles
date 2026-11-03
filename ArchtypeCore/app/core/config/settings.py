from pathlib import Path
from typing import Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.docs.fragments.headers_content import HEADERS_CONTENT

# --- Paths ---
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):

    """

    Application configuration settings using Pydantic's BaseSettings for environment variable management and validation.
    This class defines all the configuration parameters for the application, including project metadata, logging settings,
    database connection details, VPN configuration, security settings, server parameters, and CORS options.
    It also includes validators to ensure critical settings are properly configured and helper properties for convenience.

    
    Usage
    -----
    The settings can be accessed via the global `settings` instance, which will automatically load values from environment variables or the .env file.

    ```python
        from app.core.config.settings import settings
        print(settings.DATABASE_URL)  # Accessing a setting
    ```

    """

    # --- Project / API ---
    PROJECT_NAME: str = Field(default="ArchetypeCore", description="Name of the project")
    PROJECT_DESCRIPTION: str = Field(default="", description="Detailed description of the project APIs")
    VERSION: str = Field(default="0.0.1", description="Current version of the application")
    API_V1_PREFIX: str = Field(default="/api/v1", description="Prefix routing path for API v1")
    DOCS_URL: str = Field(default="/docs", description="Path for the Swagger UI documentation")
    REDOC_URL: str = Field(default="/redoc", description="Path for the ReDoc documentation")


    # --- Logging ---
    LOGGER_NAME: str = Field(default="app", description="Base name used for application loggers")
    HANDLER_LOG_LEVEL: str = Field(default="DEBUG", description="Logging level for standard output handlers")
    ROOT_LOG_LEVEL: str = Field(default="INFO", description="Logging level for the root application")
    UVICORN_LOG_LEVEL: str = Field(default="INFO", description="Logging level for the Uvicorn ASGI server")


    # --- Database ---
    DATABASE_URL: str = Field(..., description="Full database connection string (e.g., postgresql+asyncpg://...)")


    # --- External Providers / Network Abstractions ---
    SERVER_IP: str = Field(..., description="Public IP address for the external provider server")
    SERVER_PUBKEY: str = Field(..., description="Public key of the master provider server interface")
    WG_INTERFACE: str = Field(default="archetype0", description="Name of the virtual network interface")
    WG_QUICK_PATH: str = Field(default="/usr/bin/wg-quick", description="System path to the wg-quick binary")
    WG_SHOW_PATH: str = Field(default="/usr/bin/wg", description="System path to the wg binary")


    # --- Security / JWT ---
    SECRET_KEY: str = Field(..., description="Shared secret for signing tokens, at least as long as the algorithm's hash output (32 bytes for HS256)")
    ALGORITHM: str = Field(default="HS256", description="Token signature algorithm, one of HS256, HS384 and HS512")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=5, description="Minutes until an access token expires")


    # --- Server ---
    HOST: str = Field(default="0.0.0.0", description="Host address to bind the server to")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Network port for the server to listen on")
    DEBUG: bool = Field(default=False, description="Enable or disable framework-level debug mode")


    # --- CORS ---
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:8000", "http://127.0.0.1:8000"], description="List of allowed CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Whether to allow credentials in cross-origin requests")
    CORS_METHODS: list[str] = Field(default_factory=lambda: ["*"], description="List of allowed HTTP methods for CORS")
    CORS_HEADERS: list[str] = Field(default_factory=lambda: ["*"], description="List of allowed HTTP headers for CORS")


    # --- Config ---
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )


    # --- Validators ---
    @field_validator("PROJECT_DESCRIPTION", mode="before")
    @classmethod
    def append_env_description(cls, v: str | None) -> str:

        """
        
        Append environment variable info to the project description for docs.
        
        """

        default_part = HEADERS_CONTENT
        if not v:
            return default_part
        return f"{v}. {default_part}"

    @field_validator("SECRET_KEY")
    @classmethod
    def enforce_secret_key(cls, v: str) -> str:

        """

        Ensure the SECRET_KEY is set and has a minimum length for security.

        """

        if not v or len(v) < 32:
            raise ValueError(
                "SECRET_KEY must be set and at least 32 characters for production!"
            )
        return v


    @field_validator("ALGORITHM")
    @classmethod
    def enforce_hmac_algorithm(cls, v: str) -> str:

        """

        Ensure the token algorithm is one of the HMAC family, since the local adapter signs and verifies with one shared secret.

        """

        if v not in ("HS256", "HS384", "HS512"):
            raise ValueError(
                "ALGORITHM must be HS256, HS384 or HS512, because the local auth adapter signs and verifies "
                "with one shared secret; an asymmetric algorithm needs an adapter with two keys."
            )
        return v


    @model_validator(mode="after")
    def enforce_secret_length_for_algorithm(self) -> Self:

        """

        Ensure the shared secret is at least as long as the configured algorithm's hash output, as RFC 7518 requires.

        """

        needed = {"HS256": 32, "HS384": 48, "HS512": 64}[self.ALGORITHM]
        if len(self.SECRET_KEY.encode("utf-8")) < needed:
            raise ValueError(
                f"SECRET_KEY must be at least {needed} bytes for {self.ALGORITHM}, the size of its hash output."
            )
        return self


    # --- Helper properties ---
    @property
    def database_url_sync(self) -> str:

        """

        The database URL with the async driver marker stripped for synchronous tools, PostgreSQL's and SQLite's alike.

        """

        for marker, plain in (("postgresql+asyncpg://", "postgresql://"), ("sqlite+aiosqlite://", "sqlite://")):
            if self.DATABASE_URL.startswith(marker):
                return plain + self.DATABASE_URL.removeprefix(marker)
        return self.DATABASE_URL

    @property
    def is_sqlite(self) -> bool:

        """

        Whether the configured database is SQLite.

        """

        return "sqlite" in self.DATABASE_URL

    @property
    def is_production(self) -> bool:

        """

        Whether the application is running with debugging off.

        """

        return not self.DEBUG


# --- Global instance ---
settings = Settings()
