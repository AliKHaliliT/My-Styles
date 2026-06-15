from app.api.v1.schemas.devices import Device as APIDevice
from app.api.v1.schemas.devices import DeviceConfig as APIDeviceConfig
from app.domain.schemas.devices import Device as DomainDevice
from app.domain.schemas.devices import DeviceConfig as DomainDeviceConfig


def domain_to_api_device(domain: DomainDevice) -> APIDevice:

    """

    Convert Domain Device to API Device.

    """

    return APIDevice.model_validate(domain)


def domain_to_api_device_config(domain: DomainDeviceConfig) -> APIDeviceConfig:

    """
    
    Convert Domain DeviceConfig to API DeviceConfig.
    
    """

    return APIDeviceConfig.model_validate(domain)
