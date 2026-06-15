from fastapi import Depends, HTTPException, Request, status

from app.api.v1.dependencies import get_device_service
from app.api.v1.schemas.devices.device_config import DeviceConfig
from app.api.v1.translators.devices import domain_to_api_device_config
from app.services.access import DeviceService


async def get_user_config(
    request: Request,
    user_id: int,
    device_id: int,
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceConfig:
    
    """
    
    Fetches the configuration file for a specific device belonging to a user.

    """

    try:
        domain_device = await device_service.get_device_by_id(device_id=device_id)

        if not domain_device or domain_device.user_id != user_id:
            raise ValueError("Device not found for this user")

        domain_config = await device_service.get_device_config(device=domain_device)
        return domain_to_api_device_config(domain_config)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed: {e}")
