from starlette.types import ASGIApp, Receive, Scope, Send


class CrossOriginOpenerPolicyMiddleware:

    """

    ASGI middleware that adds the Cross-Origin-Opener-Policy header to all HTTP responses.

    This header helps ensure a top-level document does not share a browsing context group
    with cross-origin documents, preventing certain cross-window attacks.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import CrossOriginOpenerPolicyMiddleware

    app.add_middleware(CrossOriginOpenerPolicyMiddleware, policy="same-origin")
    ```

    """



    def __init__(self, app: ASGIApp, policy: str = "same-origin") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The COOP policy string. The default value is `"same-origin"`.
                The options are:
                    `"unsafe-none"`
                        Default, no isolation, legacy sites.
                    `"same-origin-allow-popups"`
                        Full isolation, security-sensitive pages, SharedArrayBuffer usage.
                    `"same-origin"`
                        Pages needing third-party popups but mostly isolated.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Cross-Origin-Opener-Policy header to the response.

        
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
                headers[b"cross-origin-opener-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
