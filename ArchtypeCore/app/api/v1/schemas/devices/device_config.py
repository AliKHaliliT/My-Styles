from pydantic import BaseModel, ConfigDict


class DeviceConfigBase(BaseModel):

    """

    Base API schema shared across device configuration variants.
    
    """

    config: str


class DeviceConfig(DeviceConfigBase):

    """

    API schema representing a device's configuration.
    
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "config": "[Interface]\nPrivateKey = ...\nAddress = 10.0.0.2/32\nDNS = 1.1.1.1\n\n[Peer]\nPublicKey = ...\nEndpoint = 198.51.100.1:51820\nAllowedIPs = 0.0.0.0/0, ::/0"
            }
        }
    )
