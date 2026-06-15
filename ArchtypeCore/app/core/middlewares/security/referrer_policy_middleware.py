from starlette.types import ASGIApp, Receive, Scope, Send


class ReferrerPolicyMiddleware:

    """

    ASGI middleware that adds the Referrer-Policy header to all HTTP responses.

    This header controls how much referrer information (sent via the Referer header)
    should be included with requests, enhancing user privacy.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import ReferrerPolicyMiddleware

    app.add_middleware(ReferrerPolicyMiddleware, policy="strict-origin-when-cross-origin")
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "strict-origin-when-cross-origin") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The Referrer-Policy string to be applied. Defaults to a secure and practical value.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Referrer-Policy header to the response.

        
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
                headers[b"referrer-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
