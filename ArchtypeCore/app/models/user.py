from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.device import Device


class User(Base, TimestampMixin):

    """

    Database representation of an ArchetypeCore service subscriber.

    This model is the aggregate root for a customer. It tracks 
    the user's identity, their operational status, and their cumulative 
    data transfer metrics for quota enforcement.

    """

    __tablename__ = "users"
    # The constraint stands on the table under a name, because the migration generator carries
    # a table's constraints and passes over one declared inside a column.
    __table_args__ = (CheckConstraint("status IN ('enabled', 'disabled')", name="ck_users_status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String,
        default="enabled",
        nullable=False,
    )
    quota_bytes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    used_bytes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    devices: Mapped[list[Device]] = relationship(
        "Device",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
