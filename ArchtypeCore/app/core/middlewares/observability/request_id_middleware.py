from uuid import uuid4

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.logging.log_context import request_id_var


class RequestIDMiddleware:

    """

    ASGI middleware that assigns a unique request ID to each incoming connection.

    For HTTP requests, it sets the ID in a context variable and returns it in the response header.
    For WebSocket requests, it only sets the ID for internal tracing (no response header).
    This enables consistent tracing and correlation across logs regardless of protocol.

    Note that the Request ID for the WebSocket requests are implemented but not critically tested.

    
    Usage
    -----
    ```python
    from app.core.middlewares import RequestIDMiddleware

    app.add_middleware(RequestIDMiddleware)
    ```

    """

    def __init__(self, app: ASGIApp) -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.


        Returns
        -------
        None.

        """

        self.app = app


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the incoming request, assigns a request ID,
        and ensures it is available in logs and optionally in headers.

        
        Parameters
        ----------
        scope : Scope
            The ASGI connection scope.

        receive : Receive
            Awaitable callable to receive ASGI messages.

        send : Send
            Awaitable callable to send ASGI messages.


        Returns
        -------
        None.

        """

        if scope["type"] not in {"http", "websocket"}:
            await self.app(scope, receive, send)
            return


        request = Request(scope)
        request_id = request.headers.get("x-request-id", str(uuid4()))
        token = request_id_var.set(request_id)

        async def send_wrapper(message):
            if scope["type"] == "http" and message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                headers[b"x-request-id"] = request_id.encode()
                message["headers"] = list(headers.items())
            await send(message)


        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            request_id_var.reset(token)
