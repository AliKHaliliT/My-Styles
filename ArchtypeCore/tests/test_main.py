from fastapi import status
from fastapi.testclient import TestClient

from main import app

# Booting the whole application is the point of this suite: every module under app imports
# under the warnings-as-errors gate, and one malformed request proves the validation handler
# answers in the standard error shape with the request id echoed.


def test_a_malformed_request_is_refused_in_the_standard_error_shape() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/auth/login", data={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    payload = response.json()
    assert payload["title"] == "Validation Error"
    assert payload["status_code"] == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert payload["type"] == "validation_error"
    assert payload["detail"]
    assert "x-request-id" in response.headers
