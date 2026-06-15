from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.common.mixins import IDMixin, TimeStampMixin
from app.api.v1.schemas.devices import Device
from app.utils.reorder_fields import reorder_fields


class UserBase(BaseModel):

    """

    Base API schema shared across user variants.

    """

    username: str
    quota_bytes: int = 0


class UserCreate(UserBase):

    """
    
    API schema used when creating a new user.

    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "quota_bytes": 10737418240
            }
        }
    )


@reorder_fields(TimeStampMixin)
class User(IDMixin, UserBase, TimeStampMixin):

    """
    
    API schema representing a user.
    
    """
    
    status: str
    used_bytes: int
    devices: list[Device] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "john_doe",
                "quota_bytes": 10737418240,
                "status": "enabled",
                "used_bytes": 536870912,
                "devices": [],
                "created_at": "2026-06-15T12:00:00Z",
                "updated_at": "2026-06-15T12:00:00Z"
            }
        }
    )
