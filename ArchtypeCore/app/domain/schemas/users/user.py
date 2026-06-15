from pydantic import BaseModel, ConfigDict

from app.domain.schemas.common import IDMixin, TimeStampMixin
from app.domain.schemas.devices import Device
from app.utils.reorder_fields import reorder_fields


class UserBase(BaseModel):

    """

    Base Domain schema shared across user variants.

    """

    username: str
    quota_bytes: int = 0


class UserCreate(UserBase):

    """

    Domain schema used when creating a new user.

    """

    pass


@reorder_fields(TimeStampMixin)
class User(IDMixin, UserBase, TimeStampMixin):

    """

    Domain schema representing a user.

    """

    status: str
    used_bytes: int
    devices: list[Device] = []

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):

    """
    
    Domain schema used for partial updates to a user.
    
    """
    
    username: str | None = None
    quota_bytes: int | None = None
    used_bytes: int | None = None
    status: str | None = None
