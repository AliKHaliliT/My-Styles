from uuid import UUID

from starlette.types import Message, Receive, Scope, Send

from app.core.logging.log_context import request_id_var
from app.core.middlewares.observability import RequestIDMiddleware

# The middleware is driven as the ASGI callable it is, with a scope built by hand and an
# application that records the id it ran under, so both protocols are proven without a socket.


async def receive_nothing() -> Message:
    return {"type": "http.request", "body": b"", "more_body": False}


def http_scope(headers: list[tuple[bytes, bytes]]) -> Scope:
    return {"type": "http", "method": "GET", "path": "/", "headers": headers, "query_string": b""}


def websocket_scope(headers: list[tuple[bytes, bytes]]) -> Scope:
    return {"type": "websocket", "path": "/ws", "headers": headers, "query_string": b""}


class Recorder:

    def __init__(self, answer: Message) -> None:
        self.answer = answer
        self.seen: list[str] = []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.seen.append(request_id_var.get())
        await send(self.answer)


async def drive(scope: Scope, answer: Message) -> tuple[Recorder, list[Message]]:
    sent: list[Message] = []

    async def capture(message: Message) -> None:
        sent.append(message)

    inner = Recorder(answer)
    await RequestIDMiddleware(inner)(scope, receive_nothing, capture)
    return inner, sent


RESPONSE_START: Message = {"type": "http.response.start", "status": 200, "headers": []}


async def test_an_http_request_runs_under_the_id_it_carried_and_gets_it_echoed() -> None:
    inner, sent = await drive(http_scope([(b"x-request-id", b"abc-123")]), dict(RESPONSE_START))

    assert inner.seen == ["abc-123"]
    assert (b"x-request-id", b"abc-123") in sent[0]["headers"]


async def test_an_http_request_without_an_id_is_given_a_uuid() -> None:
    inner, sent = await drive(http_scope([]), dict(RESPONSE_START))

    issued = inner.seen[0]
    UUID(issued)
    assert (b"x-request-id", issued.encode()) in sent[0]["headers"]


async def test_a_websocket_connection_reaches_the_application_under_its_id() -> None:
    inner, sent = await drive(websocket_scope([(b"x-request-id", b"socket-7")]), {"type": "websocket.accept"})

    assert inner.seen == ["socket-7"]
    assert sent == [{"type": "websocket.accept"}]


async def test_a_lifespan_scope_passes_through_untouched() -> None:
    inner, sent = await drive({"type": "lifespan"}, {"type": "lifespan.startup.complete"})

    assert inner.seen == ["unknown"]
    assert sent == [{"type": "lifespan.startup.complete"}]


async def test_the_id_does_not_outlive_the_request() -> None:
    await drive(http_scope([(b"x-request-id", b"abc-123")]), dict(RESPONSE_START))

    assert request_id_var.get() == "unknown"
