from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt

from app.core.config.settings import settings
from app.domain.interfaces.security import IAuthManager


class LocalAuthAdapter(IAuthManager):

    """

    Local implementation of the IAuthManager interface using Argon2 and JWT.


    Usage
    -----
    ```python
    from app.core.security import LocalAuthAdapter

    auth_manager = LocalAuthAdapter()
    
    # Hash a password
    hashed_password = auth_manager.get_password_hash("mysecretpassword")
    # Verify a password
    is_valid = auth_manager.verify_password("mysecretpassword", hashed_password)
    # Create a JWT token
    token = auth_manager.create_access_token({"sub": "user_id"})
    # Decode a JWT token
    payload = auth_manager.decode_access_token(token)
    ```

    """

    def __init__(self) -> None:

        """

        Initialize the authentication adapter with JWT settings and password hasher.


        Parameters
        ----------
        None.
        

        Returns
        -------
        None.

        """

        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        self.pwd_hasher = PasswordHasher(
            time_cost=2,
            memory_cost=102400,
            parallelism=8,
            hash_len=32,
            salt_len=16
        )


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        """
        
        Verify a plain password against a hashed password.


        Parameters
        ----------
        plain_password : str
            The plain text password to verify.

        hashed_password : str
            The hashed password to compare against.


        Returns
        -------
        bool
            True if the password is correct, False otherwise.

        """

        if not isinstance(plain_password, str):
            raise TypeError(f"plain_password must be a str. Received: {plain_password} with type {type(plain_password)}")
        if not isinstance(hashed_password, str):
            raise TypeError(f"hashed_password must be a str. Received: {hashed_password} with type {type(hashed_password)}")


        try:
            self.pwd_hasher.verify(hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False
        except Exception as e:
            logging.error(f"Password verification error: {e}")
            return False


    def get_password_hash(self, password: str) -> str:

        """
        
        Hash a password using Argon2.


        Parameters
        ----------
        password : str
            The plain text password to hash.

            
        Returns
        -------
        str
            The hashed password string.

        """

        if not isinstance(password, str):
            raise TypeError(f"password must be a str. Received: {password} with type {type(password)}")


        try:
            return self.pwd_hasher.hash(password)
        except Exception as e:
            logging.error(f"Password hashing error: {e}")
            raise ValueError("Failed to hash password") from e


    def create_access_token(self, data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        
        """
        
        Create a JWT access token.


        Parameters
        ----------
        data : dict[str, Any]
            The payload data to include in the token. Must contain a `"sub"` field.

        expires_delta : timedelta | None, optional
            The time delta for token expiration. If `None`, defaults to configured minutes.


        Returns
        -------
        str
            The encoded JWT access token.

        """

        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict. Received: {data} with type {type(data)}")


        to_encode = data.copy()
        if "sub" not in to_encode:
            raise ValueError("JWT payload must contain 'sub' field")

        now = datetime.now(timezone.utc)
        expire = now + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire, "iat": now})

        try:
            return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            logging.error(f"Token creation error: {e}")
            raise ValueError("Failed to create access token") from e
        

    def decode_access_token(self, token: str) -> dict[str, Any] | None:

        """
        
        Decode and verify a JWT access token.


        Parameters
        ----------
        token : str
            The JWT access token to decode.

            
        Returns
        -------
        dict[str, Any] | None
            The decoded payload data if the token is valid, otherwise None.

        """

        if not isinstance(token, str):
            raise TypeError(f"token must be a str. Received: {token} with type {type(token)}")


        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            logging.debug(f"JWT decode error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected token decode error: {e}")
            return None
