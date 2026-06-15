from starlette.types import ASGIApp, Receive, Scope, Send


class XXSSProtectionMiddleware:

    """

    ASGI middleware that adds the X-XSS-Protection header to all HTTP responses.

    This header was used to control the built-in reflective XSS auditor in older browsers.
    Modern browsers have removed this feature in favor of Content-Security-Policy.

    Primary Category: Legacy Header
    Sub-Category: Browser/Client Focused
    Reason for inclusion: This header provides a minimal, last-resort fallback against some reflective XSS attacks for users on very old browsers that do not support Content-Security-Policy. It should be set to disable the auditor (`0`) or enable block mode (`1; mode=block`).

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import XXSSProtectionMiddleware

    app.add_middleware(XXSSProtectionMiddleware)
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "0") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The X-XSS-Protection policy. Recommended value is '0' (to disable) or "1; mode=block" for legacy support.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the X-XSS-Protection header to the response.

        
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
                headers[b"x-xss-protection"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
