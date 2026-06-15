from pydantic import BaseModel


class DeviceConfigBase(BaseModel):

    """

    Base Domain schema shared across device configuration variants.
    
    """

    config: str


class DeviceConfig(DeviceConfigBase):

    """

    Domain schema representing a device's configuration.
    
    """

    pass
