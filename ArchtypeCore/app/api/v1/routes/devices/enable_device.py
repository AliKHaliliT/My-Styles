from fastapi import Depends, HTTPException, Request, status

from app.api.v1.dependencies import get_device_service
from app.api.v1.schemas.devices import Device
from app.api.v1.translators.devices import domain_to_api_device
from app.services.access import DeviceService


async def enable_device(
    request: Request,
    device_id: int,
    device_service: DeviceService = Depends(get_device_service),
) -> Device:
    
    """

    Enables a previously disabled device by its ID.

    """

    try:
        domain_device = await device_service.enable_device(device_id=device_id)
        return domain_to_api_device(domain_device)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed: {e}")
