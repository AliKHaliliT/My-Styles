from starlette.types import ASGIApp, Receive, Scope, Send


class XDNSPrefetchControlMiddleware:

    """

    ASGI middleware that adds the X-DNS-Prefetch-Control header to all HTTP responses.

    This header controls browser DNS prefetching, which can improve performance but may
    have privacy implications by leaking information about links a user might click.

    Primary Category: Legacy Header
    Sub-Category: Browser/Client Focused
    Reason for inclusion: Provides a privacy enhancement by disabling a browser feature that could potentially leak user navigation patterns to DNS servers.

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import XDNSPrefetchControlMiddleware

    app.add_middleware(XDNSPrefetchControlMiddleware, policy="off")
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "off") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The DNS prefetch policy.
                The options are:
                    `"on"`
                        Enable DNS prefetching.
                    `"off"`
                        Disable DNS prefetching.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the X-DNS-Prefetch-Control header to the response.

        
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
                headers[b"x-dns-prefetch-control"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
