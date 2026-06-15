from contextvars import ContextVar

# Holds the request ID for each individual request.
request_id_var: ContextVar[str] = ContextVar("request_id", default="unknown")
