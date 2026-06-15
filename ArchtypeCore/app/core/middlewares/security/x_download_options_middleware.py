from starlette.types import ASGIApp, Receive, Scope, Send


class XDownloadOptionsMiddleware:

    """

    ASGI middleware that adds the X-Download-Options header to all HTTP responses.

    This is a legacy, IE-specific header that forces the browser to prompt the user to
    save a file, rather than opening it directly in the browser, mitigating some phishing attacks.

    Primary Category: Legacy Header
    Sub-Category: Browser/Client Focused
    Reason for inclusion: Provides a specific security enhancement for users on Internet Explorer 8 and newer, preventing HTML files from being executed in the context of the site.

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import XDownloadOptionsMiddleware

    app.add_middleware(XDownloadOptionsMiddleware)
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

        Processes the HTTP request and appends the X-Download-Options header to the response.

        
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
                headers[b"x-download-options"] = b"noopen"
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
