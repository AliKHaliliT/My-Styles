from typing import Any

from app.domain.schemas.devices import DeviceCreate as DomainDeviceCreate
from app.domain.schemas.devices import DeviceUpdate as DomainDeviceUpdate
from app.models.device import Device as DBDevice


def domain_to_db_device_create(
    domain_obj: DomainDeviceCreate, 
    client_identifier: str, 
    protocol_data: dict[str, Any], 
    ip_address: str | None
) -> DBDevice:

    """

    Convert Domain DeviceCreate to a new Database Device model.

    """

    return DBDevice(
        user_id=domain_obj.user_id,
        device_name=domain_obj.device_name,
        client_identifier=client_identifier,
        protocol_data=protocol_data,
        ip_address=ip_address
    )


def domain_to_db_device_update(domain_obj: DomainDeviceUpdate) -> dict[str, Any]:

    """

    Convert Domain DeviceUpdate to a dictionary of Database columns, dropping None values.

    """

    update_data = {}
    
    if domain_obj.device_name is not None:
        update_data["device_name"] = domain_obj.device_name
    if domain_obj.status is not None:
        update_data["status"] = domain_obj.status
        
    return update_data
