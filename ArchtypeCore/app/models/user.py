from sqlalchemy import CheckConstraint, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base
from db.mixins import TimestampMixin


class User(Base, TimestampMixin):

    """

    Database representation of an ArchetypeCore service subscriber.

    This model serves as the aggregate root for a customer. it tracks 
    the user's identity, their operational status, and their cumulative 
    data transfer metrics for quota enforcement.

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('enabled', 'disabled')"),
        default="enabled",
        nullable=False,
    )
    quota_bytes = Column(Integer, default=0, nullable=False)
    used_bytes = Column(Integer, default=0, nullable=False)

    devices = relationship(
        "Device",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
