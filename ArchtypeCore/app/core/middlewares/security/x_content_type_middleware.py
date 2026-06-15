from starlette.types import ASGIApp, Receive, Scope, Send


class XContentTypeOptionsMiddleware:

    """

    ASGI middleware that adds the X-Content-Type-Options header to all HTTP responses.

    This header instructs the browser not to perform MIME type sniffing, which helps
    prevent certain classes of attacks, such as drive-by downloads and content-type confusion.

    Primary Category: Legacy (Still Modern)
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import XContentTypeOptionsMiddleware

    app.add_middleware(XContentTypeOptionsMiddleware)
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

        Processes the HTTP request and appends the X-Content-Type-Options header to the response.

        
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
                headers[b"x-content-type-options"] = b"nosniff"
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
