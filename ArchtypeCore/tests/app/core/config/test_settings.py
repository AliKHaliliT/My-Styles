import pytest
from pydantic import ValidationError

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


def test_an_algorithm_outside_the_hmac_family_is_refused() -> None:
    with pytest.raises(ValidationError, match="shared secret"):
        Settings(ALGORITHM="RS256")


def test_every_hmac_algorithm_is_accepted() -> None:
    assert [Settings(ALGORITHM=name).ALGORITHM for name in ("HS256", "HS384", "HS512")] == ["HS256", "HS384", "HS512"]


def test_a_secret_shorter_than_the_hash_output_is_refused() -> None:
    with pytest.raises(ValidationError, match="64 bytes"):
        Settings(ALGORITHM="HS512", SECRET_KEY="x" * 63)


def test_a_secret_as_long_as_the_hash_output_is_accepted() -> None:
    assert Settings(ALGORITHM="HS512", SECRET_KEY="x" * 64).ALGORITHM == "HS512"
