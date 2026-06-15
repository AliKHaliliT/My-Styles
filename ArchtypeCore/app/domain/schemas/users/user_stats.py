from pydantic import BaseModel

from app.domain.schemas.common import TimeStampMixin, UserIDMixin
from app.utils.reorder_fields import reorder_fields


@reorder_fields(TimeStampMixin)
class UserStatsBase(UserIDMixin, TimeStampMixin, BaseModel):

    """

    Base Domain schema shared across user stats variants.

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

    Domain schema representing a user stats.

    """

    pass
