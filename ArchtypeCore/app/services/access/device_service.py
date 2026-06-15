from app.core.config.settings import Settings
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.interfaces.vpn import IVPNProvider
from app.domain.schemas.devices import (Device, DeviceConfig, DeviceCreate,
                                        DeviceUpdate)


class DeviceService:

    """

    A highly abstracted service layer for device-related business logic.


    Usage
    -----
    This class provides methods for creating, enabling, disabling, and fetching devices.
    It relies on a Unit of Work for database interactions and an abstract Network Provider for protocol-agnostic operations.
    ```python
    from app.services.access import DeviceService

    uow = YourUnitOfWork()
    vpn_provider = YourVPNProvider()
    device_service = DeviceService(uow, vpn_provider, settings)

    # Create a new device
    new_device = await device_service.create_device(DeviceCreate(user_id=1, name="My Device"))
    # Enable a device
    enabled_device = await device_service.enable_device(new_device.id)
    # Get device config
    config = await device_service.get_device_config(enabled_device)
    print(config.config)
    ```

    """

    def __init__(
        self,
        uow: IUnitOfWork,
        vpn_provider: IVPNProvider,
        settings: Settings
    ) -> None:

        """

        Constructor for the DeviceService class.


        Parameters
        ----------
        uow : IUnitOfWork
            The Unit of Work interface for database transactions.

        vpn_provider : IVPNProvider
            The Network Provider interface.
            
        settings : Settings
            The application settings.


        Returns
        -------
        None.

        """

        if not isinstance(uow, IUnitOfWork):
            raise TypeError(f"uow must implement IUnitOfWork. Received: {uow} with type {type(uow)}")
        if not isinstance(vpn_provider, IVPNProvider):
            raise TypeError(f"vpn_provider must implement IVPNProvider. Received: {vpn_provider} with type {type(vpn_provider)}")
        if not isinstance(settings, Settings):
            raise TypeError(f"settings must be an instance of Settings. Received: {settings} with type {type(settings)}")


        self.uow = uow
        self.vpn_provider = vpn_provider
        self.settings = settings


    async def get_device_by_id(self, device_id: int) -> Device | None:

        """
        
        Fetches a single device by its ID.


        Parameters
        ----------
        device_id : int
            The ID of the device to retrieve.


        Returns
        -------
        Device | None
            The Device domain instance if found, otherwise None.
        
        """

        if not isinstance(device_id, int) or device_id <= 0:
            raise ValueError(f"device_id must be a positive integer. Received: {device_id} with type {type(device_id)}")


        async with self.uow:
            return await self.uow.devices.get(id=device_id)


    async def create_device(self, device_in: DeviceCreate) -> Device:

        """

        Creates a new device using the abstract Network Provider and UoW.


        Parameters
        ----------
        device_in : DeviceCreate
            The schema containing the data for the new device.


        Returns
        -------
        Device
            The newly created Device domain instance.

        """

        if not isinstance(device_in, DeviceCreate):
            raise TypeError(f"device_in must be a DeviceCreate. Received: {device_in} with type {type(device_in)}")


        async with self.uow:
            user = await self.uow.users.get(id=device_in.user_id)
            if not user:
                raise ValueError(f"User with ID {device_in.user_id} not found")

            # 1. Ask external interface for credentials
            client_id, protocol_data = await self.vpn_provider.generate_credentials()
            
            # 2. Ask DB interface for an IP (if applicable)
            ip_address = await self.uow.devices.get_next_ip()

            # 3. Add to Database via UoW
            device_domain = await self.uow.devices.add(
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

            # 5. Commit Transaction
            await self.uow.commit()

            return device_domain


    async def enable_device(self, device_id: int) -> Device:

        """

        Enables a device and provisions it in the network system.


        Parameters
        ----------
        device_id : int
            The ID of the device to enable.


        Returns
        -------
        Device
            The updated Device domain instance.

        """

        if not isinstance(device_id, int) or device_id <= 0:
            raise ValueError(f"device_id must be a positive integer. Received: {device_id} with type {type(device_id)}")


        async with self.uow:
            device = await self.uow.devices.get(id=device_id)
            if not device:
                raise ValueError(f"Device with ID {device_id} not found")

            await self.vpn_provider.provision_client(
                client_identifier=device.client_identifier, 
                ip_address=device.ip_address, 
                protocol_data=device.protocol_data
            )

            updated_device = await self.uow.devices.update(
                db_obj=device, 
                obj_in=DeviceUpdate(status="enabled")
            )
            await self.uow.commit()

            return updated_device


    async def disable_device(self, device_id: int) -> Device:

        """

        Disables a device and revokes it from the network system.


        Parameters
        ----------
        device_id : int
            The ID of the device to disable.


        Returns
        -------
        Device
            The updated Device domain instance.

        """

        if not isinstance(device_id, int) or device_id <= 0:
            raise ValueError(f"device_id must be a positive integer. Received: {device_id} with type {type(device_id)}")


        async with self.uow:
            device = await self.uow.devices.get(id=device_id)
            if not device:
                raise ValueError(f"Device with ID {device_id} not found")

            await self.vpn_provider.revoke_client(
                client_identifier=device.client_identifier, 
                protocol_data=device.protocol_data
            )

            updated_device = await self.uow.devices.update(
                db_obj=device, 
                obj_in=DeviceUpdate(status="disabled")
            )
            await self.uow.commit()

            return updated_device


    async def get_device_config(self, device: Device) -> DeviceConfig:

        """

        Generates a protocol-agnostic configuration string.


        Parameters
        ----------
        device : Device
            The Device domain instance.


        Returns
        -------
        DeviceConfig
            The mapped Config schema.

        """

        if not isinstance(device, Device):
            raise TypeError(f"device must be a Device. Received: {device} with type {type(device)}")


        config_str = await self.vpn_provider.get_client_config(
            client_identifier=device.client_identifier,
            ip_address=device.ip_address,
            protocol_data=device.protocol_data
        )
        return DeviceConfig(config=config_str)
