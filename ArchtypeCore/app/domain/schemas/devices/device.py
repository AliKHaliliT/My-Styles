from typing import Any

from pydantic import BaseModel, Field

from app.domain.schemas.common import IDMixin, TimeStampMixin, UserIDMixin
from app.utils.reorder_fields import reorder_fields


class DeviceBase(BaseModel):

    """
    
    Base Domain schema shared across device variants.
    
    """

    device_name: str


class DeviceCreate(UserIDMixin, DeviceBase):

    """
    
    Domain schema used when creating a new device.
    
    """
    
    pass


@reorder_fields(TimeStampMixin)
class Device(IDMixin, UserIDMixin, DeviceBase, TimeStampMixin):

    """

    Domain schema representing a device.

    """

    client_identifier: str | None = None
    protocol_data: dict[str, Any] = Field(default_factory=dict)
    ip_address: str | None = None
    status: str


class DeviceUpdate(DeviceBase):

    """
    
    Domain schema used for partial updates to a device.
    
    """
    
    device_name: str | None = None
    status: str | None = None
