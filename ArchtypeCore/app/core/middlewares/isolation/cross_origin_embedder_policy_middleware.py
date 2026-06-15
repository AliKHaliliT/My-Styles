from starlette.types import ASGIApp, Receive, Scope, Send


class CrossOriginEmbedderPolicyMiddleware:

    """

    ASGI middleware that adds the Cross-Origin-Embedder-Policy header to all HTTP responses.

    This header prevents a document from loading any cross-origin resources that do not
    explicitly grant the document permission, enabling cross-origin isolation.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import CrossOriginEmbedderPolicyMiddleware

    app.add_middleware(CrossOriginEmbedderPolicyMiddleware, policy="require-corp")
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "require-corp") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The COEP policy string. The default value is `"require-corp"`.
                The options are:
                    `"unsafe-none"`
                        Allows loading cross-origin resources without CORS; no isolation.
                    `"require-corp"`
                        Requires cross-origin resources to send CORP headers; enables full isolation for security-sensitive pages and features like SharedArrayBuffer.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Cross-Origin-Embedder-Policy header to the response.

        
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
                headers[b"cross-origin-embedder-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
