from app.core.config.settings import Settings


def test_the_sync_url_strips_the_postgresql_async_driver() -> None:
    settings = Settings(DATABASE_URL="postgresql+asyncpg://user:pw@host/db")

    assert settings.database_url_sync == "postgresql://user:pw@host/db"


def test_the_sync_url_strips_the_sqlite_async_driver() -> None:
    settings = Settings(DATABASE_URL="sqlite+aiosqlite:///./other.db")

    assert settings.database_url_sync == "sqlite:///./other.db"


def test_a_url_without_an_async_driver_passes_through_unchanged() -> None:
    settings = Settings(DATABASE_URL="postgresql://user:pw@host/db")

    assert settings.database_url_sync == "postgresql://user:pw@host/db"
