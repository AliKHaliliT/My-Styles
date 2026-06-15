from starlette.types import ASGIApp, Receive, Scope, Send


class OriginAgentClusterMiddleware:

    """

    ASGI middleware that adds the Origin-Agent-Cluster header to all HTTP responses.

    This header provides a hint to the browser that the origin should be given its own,
    separate process for performance and security isolation benefits.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import OriginAgentClusterMiddleware

    app.add_middleware(OriginAgentClusterMiddleware)
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

        Processes the HTTP request and appends the Origin-Agent-Cluster header to the response.

        
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
                headers[b"origin-agent-cluster"] = b"?1"
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
