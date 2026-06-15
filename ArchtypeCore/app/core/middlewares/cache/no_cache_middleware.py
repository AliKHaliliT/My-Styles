from starlette.types import ASGIApp, Receive, Scope, Send


class NoCacheMiddleware:

    """

    ASGI middleware that adds headers to prevent client-side caching of responses.

    This sets the Cache-Control, Pragma, and Expires headers to values that instruct
    browsers and proxies not to store the response. This is critical for sensitive data.

    Primary Category: Modern Header (with Legacy fallbacks)
    Sub-Category: API/General Client

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import NoCacheMiddleware

    app.add_middleware(NoCacheMiddleware)
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

        Processes the HTTP request and appends anti-caching headers to the response.

        
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

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                headers[b"cache-control"] = b"no-store, no-cache, must-revalidate, max-age=0"
                headers[b"pragma"] = b"no-cache"
                headers[b"expires"] = b"0"
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
