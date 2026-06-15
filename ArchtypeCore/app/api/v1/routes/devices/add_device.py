from fastapi import Depends, HTTPException, Request, status

from app.api.v1.dependencies import get_device_service
from app.api.v1.schemas.devices import Device, DeviceCreate
from app.api.v1.translators.devices import (api_to_domain_device_create,
                                            domain_to_api_device)
from app.services.access import DeviceService


async def add_device(
    request: Request,
    device_in: DeviceCreate,
    device_service: DeviceService = Depends(get_device_service),
) -> Device:
    
    """

    Provisions a new device for an existing user.
    
    """

    try:
        domain_in = api_to_domain_device_create(device_in)
        domain_device = await device_service.create_device(device_in=domain_in)
        return domain_to_api_device(domain_device)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
