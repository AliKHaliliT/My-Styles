from datetime import timedelta
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IAuthManager(Protocol):

    """
    
    Interface defining authentication and security capabilities.
    
    """

    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...
    def get_password_hash(self, password: str) -> str: ...
    def create_access_token(self, data: dict[str, Any], expires_delta: timedelta | None = None) -> str: ...
    def decode_access_token(self, token: str) -> dict[str, Any] | None: ...
