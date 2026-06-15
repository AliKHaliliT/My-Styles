from datetime import timedelta

from app.core.config.settings import Settings
from app.domain.exceptions import AuthenticationError
from app.domain.interfaces.security import IAuthManager
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.schemas.auth import AuthToken


class AuthService:

    """

    A service layer for authentication-related business logic.


    Usage
    -----
    This class provides methods for authenticating admin users and generating JWT tokens. 
    It relies on a Unit of Work for database interactions and an Authentication Manager for password verification and token creation.
    ```python
    from app.services.access import AuthService
    from app.domain.interfaces.uow import IUnitOfWork

    uow = YourUnitOfWork()
    auth_manager = YourAuthManager()
    auth_service = AuthService(uow, auth_manager, settings)
    
    token = await auth_service.authenticate_admin(username="admin1", password="secret")
    print(token.access_token)
    ```

    """

    def __init__(
        self,
        uow: IUnitOfWork,
        auth_manager: IAuthManager,
        settings: Settings
    ) -> None:

        """

        Constructor for the AuthService class.


        Parameters
        ----------
        uow : IUnitOfWork
            The Unit of Work interface for database transactions.

        auth_manager : IAuthManager
            The Authentication Manager interface.

        settings : Settings
            The application settings.


        Returns
        -------
        None.

        """

        if not isinstance(uow, IUnitOfWork):
            raise TypeError(f"uow must implement IUnitOfWork. Received: {uow} with type {type(uow)}")
        if not isinstance(auth_manager, IAuthManager):
            raise TypeError(f"auth_manager must implement IAuthManager. Received: {auth_manager} with type {type(auth_manager)}")
        if not isinstance(settings, Settings):
            raise TypeError(f"settings must be an instance of Settings. Received: {settings} with type {type(settings)}")


        self.uow = uow
        self.auth_manager = auth_manager
        self.settings = settings


    async def authenticate_admin(
        self,
        username: str,
        password: str
    ) -> AuthToken:

        """

        Authenticates an admin user and returns a JWT access token.


        Parameters
        ----------
        username : str
            The username of the admin to authenticate.

        password : str
            The password of the admin to authenticate.


        Returns
        -------
        token : AuthToken
            A domain-level schema containing the access token.

        """

        if not isinstance(username, str) or not username:
            raise ValueError(f"username must be a non-empty string. Received: {username} with type {type(username)}")
        if not isinstance(password, str):
            raise TypeError(f"password must be a string. Received: {password} with type {type(password)}")


        async with self.uow:
            admin_domain = await self.uow.admins.get_by_username(username=username)

        if not admin_domain:
            raise AuthenticationError("Incorrect username or password")

        if not self.auth_manager.verify_password(password, admin_domain.hashed_password):
            raise AuthenticationError("Incorrect username or password")

        if getattr(admin_domain, "status", "enabled") != "enabled":
            raise AuthenticationError("Account is disabled")


        access_token_expires = timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_data = {
            "sub": admin_domain.username,
            "role": getattr(admin_domain, "role", "admin"),
        }

        access_token = self.auth_manager.create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        return AuthToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
