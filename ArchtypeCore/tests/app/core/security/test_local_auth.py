from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
import pytest

from app.core.config.settings import settings
from app.core.security import LocalAuthAdapter

# The adapter signs and verifies with the one shared secret the settings hold, under the one
# algorithm they name. Each token the adapter must refuse is forged here with the library directly,
# so the refusal is the adapter's and not an accident of how the token was made.


def claims(subject: str) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {"sub": subject, "exp": now + timedelta(minutes=5), "iat": now}


def test_a_token_the_adapter_made_decodes_to_its_claims() -> None:
    adapter = LocalAuthAdapter()

    payload = adapter.decode_access_token(adapter.create_access_token({"sub": "alice", "role": "admin"}))

    assert payload is not None
    assert payload["sub"] == "alice"
    assert payload["role"] == "admin"
    assert payload["exp"] > payload["iat"]


def test_an_expired_token_is_refused() -> None:
    adapter = LocalAuthAdapter()
    token = adapter.create_access_token({"sub": "alice"}, expires_delta=timedelta(minutes=-1))

    assert adapter.decode_access_token(token) is None


def test_a_token_signed_with_another_secret_is_refused() -> None:
    token = jwt.encode(claims("alice"), "another-secret-key-of-sufficient-length-0", algorithm=settings.ALGORITHM)

    assert LocalAuthAdapter().decode_access_token(token) is None


def test_an_unsigned_token_is_refused_whatever_its_claims_say() -> None:
    token = jwt.encode(claims("alice"), "", algorithm="none")

    assert LocalAuthAdapter().decode_access_token(token) is None


def test_a_token_signed_under_another_algorithm_is_refused() -> None:
    other = "HS512" if settings.ALGORITHM != "HS512" else "HS256"
    token = jwt.encode(claims("alice"), settings.SECRET_KEY, algorithm=other)

    assert LocalAuthAdapter().decode_access_token(token) is None


def test_a_token_without_an_expiry_is_refused() -> None:
    token = jwt.encode({"sub": "alice"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    assert LocalAuthAdapter().decode_access_token(token) is None


def test_a_token_without_a_subject_is_refused() -> None:
    token = jwt.encode({"exp": datetime.now(UTC) + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    assert LocalAuthAdapter().decode_access_token(token) is None


def test_a_string_that_is_no_token_is_refused() -> None:
    assert LocalAuthAdapter().decode_access_token("not.a.token") is None


def test_a_payload_without_a_subject_makes_no_token() -> None:
    with pytest.raises(ValueError, match="sub"):
        LocalAuthAdapter().create_access_token({"role": "admin"})


def test_the_type_guards_refuse_the_wrong_types() -> None:
    adapter = LocalAuthAdapter()

    with pytest.raises(TypeError):
        adapter.create_access_token(["sub"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        adapter.decode_access_token(123)  # type: ignore[arg-type]


def test_a_password_verifies_against_its_own_hash_and_no_other() -> None:
    adapter = LocalAuthAdapter()
    digest = adapter.get_password_hash("correct horse battery staple")

    assert adapter.verify_password("correct horse battery staple", digest)
    assert not adapter.verify_password("correct horse battery stable", digest)
