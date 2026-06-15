from app.api.v1.schemas.devices import DeviceCreate as APIDeviceCreate
from app.domain.schemas.devices import DeviceCreate as DomainDeviceCreate


def api_to_domain_device_create(api_in: APIDeviceCreate) -> DomainDeviceCreate:

    """

    Convert API DeviceCreate to Domain DeviceCreate.

    """

    return DomainDeviceCreate(**api_in.model_dump())
