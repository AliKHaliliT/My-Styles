from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.security import IAuthManager
from app.domain.interfaces.uow import IUnitOfWork
from app.repositories.sqlalchemy.crud_admin import CRUDAdmin
from app.repositories.sqlalchemy.crud_device import CRUDDevice
from app.repositories.sqlalchemy.crud_user import CRUDUser
from db.session import async_session


class SQLAlchemyUnitOfWork(IUnitOfWork):

    """

    SQLAlchemy implementation of the UnitOfWork.
    Handles transactions automatically and provides access to repositories.


    Usage    
    -----
    Use as an async context manager to ensure proper transaction handling.
    ```python
    from app.repositories.sqlalchemy import SQLAlchemyUnitOfWork

    auth_manager = YourAuthManager()

    async with SQLAlchemyUnitOfWork(auth_manager) as uow:
    
        # Perform operations using uow.admins, uow.users, uow.devices
        new_user = await uow.users.add(UserCreate(username="john_doe", email="john@example.com"))
        await uow.commit()  # Commit the transaction
    ```

    """

    def __init__(self, auth_manager: IAuthManager, session_factory=async_session) -> None:

        """

        Initialize the UoW with a session factory and required adapters.


        Parameters
        ----------
        auth_manager : IAuthManager
            The authentication manager.

        session_factory : callable
            The SQLAlchemy session factory.

            
        Returns
        -------
        None.

        """

        if not isinstance(auth_manager, IAuthManager):
            raise TypeError(f"auth_manager must implement IAuthManager. Received: {auth_manager} with type {type(auth_manager)}")


        self.session_factory = session_factory
        self.auth_manager = auth_manager
        self.session: AsyncSession | None = None


    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":

        """

        Enter the async context manager, instantiating the session and repos.


        Returns
        -------
        SQLAlchemyUnitOfWork
            The active UnitOfWork instance.

        """

        self.session = self.session_factory()
        self.admins = CRUDAdmin(self.session, self.auth_manager)
        self.users = CRUDUser(self.session)
        self.devices = CRUDDevice(self.session)
        return self


    async def __aexit__(self, exc_type, exc_val, traceback) -> None:

        """

        Exit the async context manager, triggering rollback on exceptions and closing session.

        """

        if exc_type is not None:
            await self.rollback()
        
        if self.session:
            await self.session.close()


    async def commit(self) -> None:

        """

        Commit the active transaction.

        """

        if self.session:
            await self.session.commit()


    async def rollback(self) -> None:

        """

        Rollback the active transaction.

        """

        if self.session:
            await self.session.rollback()
