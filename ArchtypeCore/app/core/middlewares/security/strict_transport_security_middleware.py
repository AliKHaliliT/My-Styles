from starlette.types import ASGIApp, Receive, Scope, Send


class StrictTransportSecurityMiddleware:

    """

    This ASGI middleware adds the Strict-Transport-Security header to the response.
    It enforces secure (HTTPS) connections to the server, helping to prevent
    man-in-the-middle attacks and protocol downgrade attacks.

    Primary Category: Modern Header
    Sub-Category: API/General Client

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```
    from app.core.middlewares import StrictTransportSecurityMiddleware

    app = FastAPI()
    app.add_middleware(StrictTransportSecurityMiddleware, max_age=63072000, include_subdomains=True)
    ```

    """

    def __init__(self, app: ASGIApp, max_age: int = 63072000, include_subdomains: bool = True) -> None:

        """

        Initializes the middleware with options for HSTS configuration.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application instance.

        max_age : int
            The time (in seconds) that the browser should remember to only access the site via HTTPS. The default value is `63072000` (2 years).

        include_subdomains : bool
            Whether to apply the rule to all subdomains as well. The default value is `True`.

            
        Returns
        -------
        None.

        """

        self.app = app
        self.max_age = max_age
        self.include_subdomains = include_subdomains


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Dispatches the request through the middleware and adds the header to the response.

        
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
                value = f"max-age={self.max_age}"
                if self.include_subdomains:
                    value += "; includeSubDomains"

                headers = dict(message.get("headers", []))
                headers[b"strict-transport-security"] = value.encode("latin-1")
                message["headers"] = list(headers.items())

            await send(message)


        await self.app(scope, receive, send_wrapper)
