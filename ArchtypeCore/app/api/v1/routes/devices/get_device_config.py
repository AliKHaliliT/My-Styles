from fastapi import Depends, HTTPException, Request, status

from app.api.v1.dependencies import get_device_service
from app.api.v1.schemas.devices.device_config import DeviceConfig
from app.api.v1.translators.devices import domain_to_api_device_config
from app.services.access import DeviceService


async def get_device_config(
    request: Request,
    device_id: int,
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceConfig:
    
    """

    Retrieves the client configuration file for a specific device.

    """

    domain_device = await device_service.get_device_by_id(device_id=device_id)

    if not domain_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    domain_config = await device_service.get_device_config(domain_device)
    return domain_to_api_device_config(domain_config)
