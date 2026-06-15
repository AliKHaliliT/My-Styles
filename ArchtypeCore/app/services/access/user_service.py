import asyncio

from app.domain.interfaces.uow import IUnitOfWork
from app.domain.interfaces.vpn import IVPNProvider
from app.domain.schemas.devices import DeviceCreate, DeviceUpdate
from app.domain.schemas.users import User, UserCreate, UserStats, UserUpdate


class UserService:

    """

    A service layer for user-related business logic.


    Usage
    -----
    This class provides methods for creating users, enabling/disabling users and their devices, and fetching user statistics.
    It relies on a Unit of Work for database interactions and an abstract Network Provider for protocol-agnostic operations.
    ```python
    from app.services.access import UserService

    uow = YourUnitOfWork()
    vpn_provider = YourVPNProvider()
    user_service = UserService(uow, vpn_provider, settings)

    # Create a new user with an initial device
    new_user = await user_service.create_user_with_device(UserCreate(username="user1", password="secret"))
    # Enable the user
    enabled_user = await user_service.enable_user(new_user.id)
    # Get user statistics
    stats = await user_service.get_user_stats(enabled_user.id)
    print(stats)
    ```

    """

    def __init__(
        self,
        uow: IUnitOfWork,
        vpn_provider: IVPNProvider,
    ) -> None:

        """

        Constructor for the UserService class.


        Parameters
        ----------
        uow : IUnitOfWork
            The Unit of Work interface for database transactions.

        vpn_provider : IVPNProvider
            The Network Provider interface.


        Returns
        -------
        None.

        """

        if not isinstance(uow, IUnitOfWork):
            raise TypeError(f"uow must implement IUnitOfWork. Received: {uow} with type {type(uow)}")
        if not isinstance(vpn_provider, IVPNProvider):
            raise TypeError(f"vpn_provider must implement IVPNProvider. Received: {vpn_provider} with type {type(vpn_provider)}")


        self.uow = uow
        self.vpn_provider = vpn_provider


    async def get_user_by_id(self, user_id: int) -> User | None:

        """

        Fetches a single user by their ID.


        Parameters
        ----------
        user_id : int
            The ID of the user to retrieve.


        Returns
        -------
        User | None
            The domain schema for the user if found, otherwise None.

        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError(f"user_id must be a positive integer. Received: {user_id} with type {type(user_id)}")


        async with self.uow:
            return await self.uow.users.get(id=user_id)


    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:

        """

        Fetches a list of all users.


        Parameters
        ----------
        skip : int, optional
            The number of users to skip.

        limit : int, optional
            The maximum number of users to return.


        Returns
        -------
        list[User]
            A list of domain-level user schemas.

        """

        if not isinstance(skip, int) or skip < 0:
            raise ValueError(f"skip must be a non-negative integer. Received: {skip} with type {type(skip)}")
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError(f"limit must be a positive integer. Received: {limit} with type {type(limit)}")


        async with self.uow:
            return await self.uow.users.get_multi(skip=skip, limit=limit)


    async def create_user_with_device(
        self,
        user_in: UserCreate,
        initial_device_name: str = "initial_device",
    ) -> User:

        """

        Creates a new user and provisions an initial device for them.


        Parameters
        ----------
        user_in : UserCreate
            The schema containing the data for the new user.

        initial_device_name : str, optional
            The name for the user's first device.


        Returns
        -------
        User
            The domain schema for the newly created user.

        """

        if not isinstance(user_in, UserCreate):
            raise TypeError(f"user_in must be a UserCreate. Received: {user_in} with type {type(user_in)}")
        if not isinstance(initial_device_name, str) or not initial_device_name.strip():
            raise ValueError(f"initial_device_name must be a non-empty string. Received: {initial_device_name} with type {type(initial_device_name)}")


        async with self.uow:
            existing = await self.uow.users.get_by_username(username=user_in.username)
            if existing:
                raise ValueError(f"User with username '{user_in.username}' already exists")

            user_domain = await self.uow.users.add(entity_in=user_in)

            # 1. Ask external interface for credentials
            client_id, protocol_data = await self.vpn_provider.generate_credentials()
            
            # 2. Ask DB interface for an IP
            ip_address = await self.uow.devices.get_next_ip()

            # 3. Add to Database via UoW
            device_in = DeviceCreate(user_id=user_domain.id, device_name=initial_device_name)
            await self.uow.devices.add(
                entity_in=device_in,
                client_identifier=client_id,
                protocol_data=protocol_data,
                ip_address=ip_address
            )

            # 4. Provision in network system
            await self.vpn_provider.provision_client(
                client_identifier=client_id, 
                ip_address=ip_address, 
                protocol_data=protocol_data
            )

            await self.uow.commit()

            return await self.uow.users.get(id=user_domain.id)


    async def _update_user_and_device_status(
        self,
        user_id: int,
        status: str,
    ) -> User:
        
        """

        A generic helper to update the status of a user and their devices.


        Parameters
        ----------
        user_id : int
            The ID of the user.

        status : str
            The new status to apply.


        Returns
        -------
        User
            The updated domain schema.

        """

        async with self.uow:
            user_domain = await self.uow.users.get(id=user_id)
            if not user_domain:
                raise ValueError(f"User with ID {user_id} not found")

            vpn_tasks =[]
            
            for device in user_domain.devices:
                if device.status != status:
                    await self.uow.devices.update(
                        db_obj=device, 
                        obj_in=DeviceUpdate(status=status)
                    )
                    
                    if status == "enabled":
                        vpn_tasks.append(asyncio.to_thread(
                            self.vpn_provider.provision_client, 
                            device.client_identifier, 
                            device.ip_address, 
                            device.protocol_data
                        ))
                    else:
                        vpn_tasks.append(asyncio.to_thread(
                            self.vpn_provider.revoke_client, 
                            device.client_identifier, 
                            device.protocol_data
                        ))
            
            if vpn_tasks:
                await asyncio.gather(*vpn_tasks)

            updated_user = await self.uow.users.update(
                db_obj=user_domain, 
                obj_in=UserUpdate(status=status)
            )
            await self.uow.commit()

            return updated_user


    async def enable_user(self, user_id: int) -> User:

        """

        Enables a user and all their associated devices.


        Parameters
        ----------
        user_id : int
            The ID of the user to enable.


        Returns
        -------
        User
            The domain schema for the updated user.

        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError(f"user_id must be a positive integer. Received: {user_id} with type {type(user_id)}")


        return await self._update_user_and_device_status(user_id, "enabled")


    async def disable_user(self, user_id: int) -> User:

        """

        Disables a user and all their associated devices.


        Parameters
        ----------
        user_id : int
            The ID of the user to disable.


        Returns
        -------
        User
            The domain schema for the updated user.

        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError(f"user_id must be a positive integer. Received: {user_id} with type {type(user_id)}")


        return await self._update_user_and_device_status(user_id, "disabled")


    async def get_user_stats(self, user_id: int) -> UserStats:

        """

        Computes and returns statistics for a given user.

        
        Parameters
        ----------
        user_id : int
            The ID of the user for which to generate statistics.

            
        Returns
        -------
        UserStats
            A domain-level schema containing user statistics.

        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError(f"user_id must be a positive integer. Received: {user_id} with type {type(user_id)}")


        async with self.uow:
            domain_user = await self.uow.users.get(id=user_id)
            if not domain_user:
                raise TypeError(f"User with ID {user_id} not found.")

        total_devices = len(domain_user.devices)
        enabled_devices = sum(1 for d in domain_user.devices if d.status == "enabled")

        quota_usage = 0.0
        if domain_user.quota_bytes and domain_user.quota_bytes > 0:
            quota_usage = (domain_user.used_bytes / domain_user.quota_bytes) * 100


        return UserStats(
            user_id=domain_user.id,
            username=domain_user.username,
            status=domain_user.status,
            used_bytes=domain_user.used_bytes,
            quota_bytes=domain_user.quota_bytes,
            quota_usage_percent=round(quota_usage, 2),
            total_devices=total_devices,
            enabled_devices=enabled_devices,
            disabled_devices=total_devices - enabled_devices,
            created_at=domain_user.created_at,
            updated_at=domain_user.updated_at,
        )
