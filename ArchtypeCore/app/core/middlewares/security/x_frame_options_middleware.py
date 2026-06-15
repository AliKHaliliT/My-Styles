from starlette.types import ASGIApp, Receive, Scope, Send


class XFrameOptionsMiddleware:

    """

    ASGI middleware that adds the X-Frame-Options header to all HTTP responses.

    This header helps to protect against "clickjacking" attacks by indicating whether
    a browser should be allowed to render a page in a <frame>, <iframe>, <embed> or <object>.

    Primary Category: Legacy Header
    Sub-Category: Browser/Client Focused
    Reason for inclusion: This header provides a fallback layer of protection against clickjacking attacks for older browsers that do not support the modern Content-Security-Policy `frame-ancestors` directive.

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import XFrameOptionsMiddleware

    app.add_middleware(XFrameOptionsMiddleware, policy="DENY")
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "DENY") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The X-Frame-Options policy. The default value is `"DENY"`.
                The options are:
                    `"DENY"`
                        Prevents the page from being displayed in a frame, iframe, or object, regardless of origin.
                    `"SAMEORIGIN"`
                        Allows the page to be displayed in a frame only if the framing page is from the same origin.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the X-Frame-Options header to the response.

        
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
                headers[b"x-frame-options"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
