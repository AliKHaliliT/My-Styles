from starlette.types import ASGIApp, Receive, Scope, Send


class ContentSecurityPolicyMiddleware:

    """

    ASGI middleware that adds the Content-Security-Policy header to all HTTP responses.

    This header is a powerful tool to prevent Cross-Site Scripting (XSS), clickjacking,
    and other code injection attacks by specifying the domains that the browser
    should consider to be valid sources of executable scripts.

    Primary Category: Modern Header
    Sub-Category: Browser/Client Focused

    Note that this middleware only handles HTTP requests and is implemented in ASGI manner for consistency and to avoid silent failures.

    
    Usage
    -----
    ```python
    from app.core.middlewares import ContentSecurityPolicyMiddleware

    policy = "default-src 'self'; script-src 'self' [https://trusted.cdn.com](https://trusted.cdn.com);"
    app.add_middleware(ContentSecurityPolicyMiddleware, policy=policy)
    ```

    """

    def __init__(self, app: ASGIApp, policy: str = "default-src 'self'") -> None:

        """

        Initialize the middleware with the given ASGI application.

        
        Parameters
        ----------
        app : ASGIApp
            The ASGI application to wrap.
        
        policy : str
            The CSP policy string to be applied. The default value is `"default-src 'self'"`.


        Returns
        -------
        None.

        """

        self.app = app
        self.policy = policy


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        """

        Processes the HTTP request and appends the Content-Security-Policy header to the response.

        
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
                headers[b"content-security-policy"] = self.policy.encode("latin-1")
                message["headers"] = list(headers.items())
            await send(message)


        await self.app(scope, receive, send_wrapper)
