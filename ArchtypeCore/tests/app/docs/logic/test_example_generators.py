from typing import Any

import pytest
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from app.docs.logic.example_generators import (generate_example_from_exception,
                                               generate_example_from_pydantic)


class Inner(BaseModel):
    count: int
    label: str


class Outer(BaseModel):
    name: str
    ratio: float
    flag: bool
    inner: Inner
    items: list[Inner]
    tags: list[str]
    maybe: Inner | None
    note: str | None = None
    blob: dict[str, Any]


class Described(Exception):

    def __init__(self) -> None:
        super().__init__("described")
        self.status_code = 418
        self.detail = "a teapot"
        self.payload = object()


def test_a_pydantic_model_becomes_an_example_that_follows_its_schema() -> None:
    example = generate_example_from_pydantic(Outer)

    assert example == {
        "name": "string",
        "ratio": 1.0,
        "flag": True,
        "inner": {"count": 1, "label": "string"},
        "items": [{"count": 1, "label": "string"}],
        "tags": ["string"],
        "maybe": {"count": 1, "label": "string"},
        "note": "string",
        "blob": {},
    }


def test_anything_but_a_model_class_is_refused() -> None:
    with pytest.raises(TypeError, match="Pydantic model class"):
        generate_example_from_pydantic(Outer(name="n", ratio=1.0, flag=True, inner=Inner(count=1, label="l"), items=[], tags=[], maybe=None, blob={}))  # type: ignore[arg-type]


def test_an_exception_instance_yields_its_serializable_public_attributes() -> None:
    example = generate_example_from_exception(Described())

    assert example == {"status_code": 418, "detail": "a teapot"}


def test_the_validation_error_class_yields_the_hand_written_example() -> None:
    example = generate_example_from_exception(RequestValidationError)

    assert example["status_code"] == 422
    assert example["detail"][0]["loc"] == ["body", "field_name"]


def test_anything_but_an_exception_is_refused() -> None:
    with pytest.raises(TypeError, match="Expected an exception instance"):
        generate_example_from_exception("not an exception")  # type: ignore[arg-type]
