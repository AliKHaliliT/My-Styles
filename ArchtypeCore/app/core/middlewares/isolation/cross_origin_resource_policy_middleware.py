from starlette.types import ASGIApp, Receive, Scope, Send


class CrossOriginResourcePolicyMiddleware:

    """

    ASGI middleware that adds the Cross-Origin-Resource-Policy header to all HTTP responses.

    This header informs the browser whether a resource should be allowed to be loaded by
    cross-origin documents, protecting against side-channel attacks like Spectre.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import CrossOriginResourcePolicyMiddleware

    app.add_middleware(CrossOriginResourcePolicyMiddleware, policy="same-origin")
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
            The CORP policy string. The default value is `"same-origin"`.
                The options are:
                    `"same-site"`
                        Only allow the resource to be loaded by documents from the same origin.
                    `"same-origin"`
                        Allow the resource to be loaded by documents from the same site (same eTLD+1).
                    `"cross-origin"`
                        Allow the resource to be loaded by any origin.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Cross-Origin-Resource-Policy header to the response.

        
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
                headers[b"cross-origin-resource-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
