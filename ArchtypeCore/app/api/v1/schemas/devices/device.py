from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.common.mixins import (IDMixin, TimeStampMixin,
                                              UserIDMixin)
from app.utils.reorder_fields import reorder_fields


class DeviceBase(BaseModel):

    """
    
    Base API schema shared across device variants.
    
    """
    
    device_name: str


class DeviceCreate(UserIDMixin, DeviceBase):

    """
    
    API schema used when creating a new device.
    
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "device_name": "mobile_phone"
            }
        }
    )


@reorder_fields(TimeStampMixin)
class Device(IDMixin, UserIDMixin, DeviceBase, TimeStampMixin):

    """

    API schema representing a device.

    """

    client_identifier: str | None = None
    ip_address: str | None = None
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "device_name": "mobile_phone",
                "client_identifier": "xYz123aBc456...",
                "ip_address": "10.0.0.2",
                "status": "enabled",
                "created_at": "2026-06-15T12:00:00Z",
                "updated_at": "2026-06-15T12:00:00Z"
            }
        }
    )
