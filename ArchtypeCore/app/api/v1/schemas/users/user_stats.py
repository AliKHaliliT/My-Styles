from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.common.mixins import TimeStampMixin, UserIDMixin
from app.utils.reorder_fields import reorder_fields


@reorder_fields(TimeStampMixin)
class UserStatsBase(UserIDMixin, TimeStampMixin, BaseModel):

    """

    Base API schema shared across user stats variants.

    """

    username: str
    status: str
    used_bytes: int | None = None
    quota_bytes: int | None = None
    quota_usage_percent: float
    total_devices: int
    enabled_devices: int
    disabled_devices: int


class UserStats(UserStatsBase):

    """

    API schema representing a user stats.

    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "username": "john_doe",
                "status": "enabled",
                "used_bytes": 536870912,
                "quota_bytes": 10737418240,
                "quota_usage_percent": 5.0,
                "total_devices": 2,
                "enabled_devices": 2,
                "disabled_devices": 0,
                "created_at": "2026-06-15T12:00:00Z",
                "updated_at": "2026-06-15T12:00:00Z"
            }
        }
    )
