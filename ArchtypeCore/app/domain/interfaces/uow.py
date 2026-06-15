from typing import Protocol, runtime_checkable

from app.domain.interfaces.repositories import (IAdminRepository,
                                                IDeviceRepository,
                                                IUserRepository)


@runtime_checkable
class IUnitOfWork(Protocol):

    """

    Interface defining the Unit of Work for transactional boundary management.

    """

    admins: IAdminRepository
    users: IUserRepository
    devices: IDeviceRepository

    async def __aenter__(self) -> "IUnitOfWork": ...
    async def __aexit__(self, exc_type, exc_val, traceback) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
