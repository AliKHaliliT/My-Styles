from starlette.types import ASGIApp, Receive, Scope, Send


class PermissionsPolicyMiddleware:

    """

    ASGI middleware that adds the Permissions-Policy header to all HTTP responses.

    This header provides a mechanism to selectively enable, disable, and modify the
    behavior of certain browser features and APIs on a website, such as camera,
    microphone, and geolocation access.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import PermissionsPolicyMiddleware

    policy = "camera=(), microphone=(), geolocation=()"
    app.add_middleware(PermissionsPolicyMiddleware, policy=policy)
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "camera=(), microphone=(), geolocation=()") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The Permissions-Policy string to be applied. Defaults to disabling common sensitive features.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Permissions-Policy header to the response.

        
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
                headers[b"permissions-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
