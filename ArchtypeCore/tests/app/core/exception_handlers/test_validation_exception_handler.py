import json
from typing import cast

import pytest
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError, field_validator

from app.core.exception_handlers.validation_exception_handler import validation_exception_handler

# A validator that refuses a value raises, and the error it leaves keeps the exception in its
# context. The handler is called as a plain function, since no request of the application's own
# reaches a validator that raises.


class Named(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def refuse_a_blank_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a blank name is refused")
        return value


async def test_a_value_a_validator_refuses_is_answered_as_unprocessable_with_its_reason() -> None:
    with pytest.raises(ValidationError) as refused:
        Named(name=" ")

    response = await validation_exception_handler(cast(Request, None), RequestValidationError(refused.value.errors()))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    payload = json.loads(bytes(response.body))
    assert payload["type"] == "validation_error"
    assert payload["detail"][0]["ctx"]["error"] == "a blank name is refused"
