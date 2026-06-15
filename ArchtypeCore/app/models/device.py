from sqlalchemy import (JSON, CheckConstraint, Column, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import relationship

from db.base import Base
from db.mixins import TimestampMixin


class Device(Base, TimestampMixin):

    """

    Database representation of a connected client or tunnel profile.

    This model is protocol-agnostic. It stores a generic client identifier 
    and a JSON block for protocol-specific secrets (like private keys or 
    certificates), allowing the system to support multiple implementations.

    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_name = Column(Text, nullable=False)
    
    # Protocol Agnostic Fields
    client_identifier = Column(String, unique=True, nullable=False, index=True)
    protocol_data = Column(JSON, nullable=False, default=dict)
    ip_address = Column(String, unique=True, nullable=True)
    
    status = Column(
        String,
        CheckConstraint("status IN ('enabled', 'disabled')"),
        default="enabled",
        nullable=False,
    )

    user = relationship("User", back_populates="devices")
