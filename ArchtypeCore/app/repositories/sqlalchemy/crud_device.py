from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.repositories import IDeviceRepository
from app.domain.schemas.devices import Device as DomainDevice
from app.domain.schemas.devices import DeviceCreate as DomainDeviceCreate
from app.domain.schemas.devices import DeviceUpdate as DomainDeviceUpdate
from app.models.device import Device as DBDevice
from app.models.user import User as DBUser
from app.repositories.translators.devices import (db_to_domain_device,
                                                  domain_to_db_device_create,
                                                  domain_to_db_device_update)


class CRUDDevice(IDeviceRepository):

    """

    SQLAlchemy implementation of the IDeviceRepository.


    Usage
    -----
    This class provides methods to perform CRUD operations on Device entities
    using an asynchronous SQLAlchemy session.
    ```python
    from app.repositories.sqlalchemy import CRUDDevice
    from app.domain.schemas.devices import DeviceCreate, DeviceUpdate

    async with AsyncSession(engine) as session:
    
        device_repo = CRUDDevice(session)
    
        # Create a new device
        new_device = await device_repo.add(DeviceCreate(user_id=1, device_name="My VPN Device"), "client123", {"key": "value"}, "device_config")
        # Get a device by ID
        device = await device_repo.get(new_device.id)
        # Update a device
        updated_device = await device_repo.update(device, DeviceUpdate(device_name="Updated VPN Device"))
        # Delete a device
        deleted_device = await device_repo.delete(updated_device.id)
    ```

    """

    def __init__(self, session: AsyncSession) -> None:

        """
        
        Initialize with AsyncSession.


        Parameters
        ----------
        session : AsyncSession
            The SQLAlchemy asynchronous session.

            
        Returns
        -------
        None.
        
        """

        if not isinstance(session, AsyncSession):
            raise TypeError(f"session must be an AsyncSession. Received: {session} with type {type(session)}")


        self.session = session
        self.model = DBDevice


    async def get(self, id: Any) -> DomainDevice | None:

        """
        
        Retrieve a Device by ID.


        Parameters
        ----------
        id : Any
            The ID of the device.

            
        Returns
        -------
        DomainDevice | None
            The mapped domain schema, or None if not found.
        
        """

        db_obj = await self.session.scalar(select(self.model).where(self.model.id == id))
        return db_to_domain_device(db_obj) if db_obj else None


    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[DomainDevice]:
        
        """
        
        Retrieve all devices with pagination.


        Parameters
        ----------
        skip : int
            Number of records to skip.

        limit : int
            Maximum number of records to return.

            
        Returns
        -------
        list[DomainDevice]
            A list of mapped domain schemas.
        
        """

        if not isinstance(skip, int):
            raise TypeError(f"skip must be an int. Received: {skip} with type {type(skip)}")
        if not isinstance(limit, int):
            raise TypeError(f"limit must be an int. Received: {limit} with type {type(limit)}")


        db_objs = await self.session.scalars(select(self.model).offset(skip).limit(limit))
        return[db_to_domain_device(obj) for obj in db_objs]


    async def get_multi_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[DomainDevice]:
        
        """
        
        Retrieve all devices belonging to a specific user.


        Parameters
        ----------
        user_id : int
            The ID of the user.

        skip : int
            Number of records to skip.

        limit : int
            Maximum number of records to return.

            
        Returns
        -------
        list[DomainDevice]
            A list of mapped domain schemas.
        
        """

        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be an int. Received: {user_id} with type {type(user_id)}")
        if not isinstance(skip, int):
            raise TypeError(f"skip must be an int. Received: {skip} with type {type(skip)}")
        if not isinstance(limit, int):
            raise TypeError(f"limit must be an int. Received: {limit} with type {type(limit)}")


        db_objs = await self.session.scalars(select(self.model).where(self.model.user_id == user_id).offset(skip).limit(limit))
        return[db_to_domain_device(obj) for obj in db_objs]


    async def get_enabled_devices_with_enabled_users(self) -> list[DomainDevice]:

        """
        
        Retrieve devices that are enabled and belong to enabled users.


        Parameters
        ----------
        None.

            
        Returns
        -------
        list[DomainDevice]
            A list of mapped domain schemas.
        
        """

        db_objs = await self.session.scalars(
            select(self.model).join(DBUser).where(
                DBUser.status == "enabled",
                self.model.status == "enabled"
            )
        )
        return[db_to_domain_device(obj) for obj in db_objs]


    async def get_next_ip(self) -> str:

        """

        Helper to compute the next available IP address.


        Parameters
        ----------
        None.

            
        Returns
        -------
        str
            The next available IP string.

        """
        
        last_ip = await self.session.scalar(select(self.model.ip_address).order_by(self.model.id.desc()))

        if not last_ip:
            return "10.0.0.2"

        ip_parts = last_ip.split(".")
        next_ip_int = int(ip_parts[3]) + 1

        if next_ip_int > 254:
            raise RuntimeError("IP address space exhausted.")
        
        return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{next_ip_int}"


    async def add(self, entity_in: DomainDeviceCreate, client_identifier: str, protocol_data: dict[str, Any], ip_address: str | None) -> DomainDevice:

        """

        Add a new Device record.


        Parameters
        ----------
        entity_in : DomainDeviceCreate
            The domain schema for creation.

        client_identifier : str
            The abstract identifier for the VPN client.

        protocol_data : dict[str, Any]
            The VPN protocol specific data.

        ip_address : str | None
            The allocated IP address.

            
        Returns
        -------
        DomainDevice
            The newly created mapped domain schema.

        """

        if not isinstance(entity_in, DomainDeviceCreate):
            raise TypeError(f"entity_in must be a DomainDeviceCreate. Received: {entity_in} with type {type(entity_in)}")
        if not isinstance(client_identifier, str):
            raise TypeError(f"client_identifier must be a str. Received: {client_identifier} with type {type(client_identifier)}")
        if not isinstance(protocol_data, dict):
            raise TypeError(f"protocol_data must be a dict. Received: {protocol_data} with type {type(protocol_data)}")


        db_obj = domain_to_db_device_create(
            domain_obj=entity_in,
            client_identifier=client_identifier,
            protocol_data=protocol_data,
            ip_address=ip_address
        )
        
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)

        return db_to_domain_device(db_obj)


    async def update(self, db_obj: DomainDevice, obj_in: DomainDeviceUpdate) -> DomainDevice:

        """

        Update a Device record.


        Parameters
        ----------
        db_obj : DomainDevice
            The existing domain representation.

        obj_in : DomainDeviceUpdate
            The domain schema containing updates to apply.

            
        Returns
        -------
        DomainDevice
            The updated mapped domain schema.

        """

        if not isinstance(db_obj, DomainDevice):
            raise TypeError(f"db_obj must be a DomainDevice. Received: {db_obj} with type {type(db_obj)}")
        if not isinstance(obj_in, DomainDeviceUpdate):
            raise TypeError(f"obj_in must be a DomainDeviceUpdate. Received: {obj_in} with type {type(obj_in)}")


        db_model = await self.session.scalar(select(self.model).where(self.model.id == db_obj.id))
        if not db_model:
            raise NoResultFound(f"Device with id {db_obj.id} not found")

        update_data = domain_to_db_device_update(domain_obj=obj_in)

        for field, value in update_data.items():
            if hasattr(db_model, field):
                setattr(db_model, field, value)

        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model)

        return db_to_domain_device(db_model)


    async def delete(self, id: int) -> DomainDevice:

        """

        Delete a Device by ID.


        Parameters
        ----------
        id : int
            The ID of the device.

            
        Returns
        -------
        DomainDevice
            The deleted mapped domain schema.

        """

        if not isinstance(id, int):
            raise TypeError(f"id must be an int. Received: {id} with type {type(id)}")


        db_model = await self.session.scalar(select(self.model).where(self.model.id == id))
        if db_model is None:
            raise NoResultFound(f"Device with id {id} not found")

        domain_obj = db_to_domain_device(db_model)
        await self.session.delete(db_model)
        await self.session.flush()

        return domain_obj
