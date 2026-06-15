from logging import getLogger
import time

from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.config.settings import settings

# Custom access logger for the application
app_access_logger = getLogger(f"{settings.LOGGER_NAME}.access")



class AccessLogMiddleware:

    """

    ASGI middleware to log access details for HTTP and WebSocket requests.

    For HTTP, it logs request method, path, status code, and processing time.
    For WebSocket, it logs the initial handshake and connection metadata.
    Useful for monitoring traffic and debugging.
    
    Note that the Logging for the WebSocket requests are implemented but not critically tested.

    
    Usage
    -----
    ```python
    from app.core.middlewares import AccessLogMiddleware

    app.add_middleware(AccessLogMiddleware)
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

        Handles the incoming request, logs access information,
        and forwards the response or connection.

        
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


        start_time = time.time()
        client = scope.get("client") or ("-", "-")
        path_with_query = scope.get("path", "")
        if scope.get("query_string"):
            path_with_query += f"?{scope['query_string'].decode()}"

        if scope["type"] == "websocket":
            # Log WebSocket connection handshake
            app_access_logger.info(
                f"{client[0]}:{client[1]} - "
                f"'WebSocket CONNECT {path_with_query}'"
            )
            await self.app(scope, receive, send)
            return


        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = (time.time() - start_time) * 1000

                # Log the HTTP access entry
                app_access_logger.info(
                    f"{client[0]}:{client[1]} - "
                    f"'{scope['method']} {path_with_query} HTTP/{scope['http_version']}' "
                    f"{message['status']}",
                    extra={"process_time_ms": f"{process_time:.2f}"}
                )

            await send(message)


        await self.app(scope, receive, send_wrapper)
