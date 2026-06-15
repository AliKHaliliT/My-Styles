from pathlib import Path

from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings

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
    PROJECT_DESCRIPTION: str = Field(default=None, description="Detailed description of the project APIs")
    VERSION: str = Field(default="1.0.0", description="Current version of the application")
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
    SECRET_KEY: str = Field(..., description="Cryptographic secret key for signing JWTs (must be ≥32 characters)")
    ALGORITHM: str = Field(default="HS256", description="Hashing algorithm used for token signatures")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=5, description="Minutes until an access token expires")


    # --- Server ---
    HOST: str = Field(default="0.0.0.0", description="Host address to bind the server to")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Network port for the server to listen on")
    DEBUG: bool = Field(default=False, description="Enable or disable framework-level debug mode")


    # --- CORS ---
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"], description="List of allowed CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Whether to allow credentials in cross-origin requests")
    CORS_METHODS: list[str] = Field(default_factory=lambda: ["*"], description="List of allowed HTTP methods for CORS")
    CORS_HEADERS: list[str] = Field(default_factory=lambda: ["*"], description="List of allowed HTTP headers for CORS")


    # --- Config ---
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )


    # --- Validators ---
    @field_validator("PROJECT_DESCRIPTION", mode="before")
    @classmethod
    def append_env_description(cls, v):

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


    # --- Helper properties ---
    @property
    def database_url_sync(self) -> str:
        if self.DATABASE_URL.startswith("postgresql+asyncpg://"):
            return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        return self.DATABASE_URL

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.DATABASE_URL

    @property
    def is_production(self) -> bool:
        return not self.DEBUG


# --- Global instance ---
settings = Settings()
