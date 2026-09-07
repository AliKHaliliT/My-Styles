import logging

import pytest
from starlette.types import Message, Receive, Scope, Send

from app.core.middlewares.observability import AccessLogMiddleware
from app.core.middlewares.observability.access_log_middleware import app_access_logger


async def receive_nothing() -> Message:
    return {"type": "http.request", "body": b"", "more_body": False}


class Answering:

    def __init__(self, answer: Message) -> None:
        self.answer = answer
        self.reached = False

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.reached = True
        await send(self.answer)


async def drive(scope: Scope, answer: Message) -> Answering:
    async def swallow(message: Message) -> None:
        return None

    inner = Answering(answer)
    await AccessLogMiddleware(inner)(scope, receive_nothing, swallow)
    return inner


async def test_an_http_response_is_logged_with_its_status_and_timing(caplog: pytest.LogCaptureFixture) -> None:
    scope: Scope = {
        "type": "http",
        "method": "GET",
        "path": "/users",
        "query_string": b"page=2",
        "http_version": "1.1",
        "client": ("10.0.0.7", 51000),
        "headers": [],
    }
    with caplog.at_level(logging.INFO, logger=app_access_logger.name):
        await drive(scope, {"type": "http.response.start", "status": 200, "headers": []})

    assert [record.getMessage() for record in caplog.records] == ["10.0.0.7:51000 - 'GET /users?page=2 HTTP/1.1' 200"]
    assert hasattr(caplog.records[0], "process_time_ms")


async def test_a_websocket_handshake_is_logged_and_handed_on(caplog: pytest.LogCaptureFixture) -> None:
    scope: Scope = {"type": "websocket", "path": "/ws", "query_string": b"", "client": ("10.0.0.7", 51001), "headers": []}
    with caplog.at_level(logging.INFO, logger=app_access_logger.name):
        inner = await drive(scope, {"type": "websocket.accept"})

    assert inner.reached
    assert [record.getMessage() for record in caplog.records] == ["10.0.0.7:51001 - 'WebSocket CONNECT /ws'"]


async def test_a_lifespan_scope_is_neither_logged_nor_blocked(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger=app_access_logger.name):
        inner = await drive({"type": "lifespan"}, {"type": "lifespan.startup.complete"})

    assert inner.reached
    assert caplog.records == []
