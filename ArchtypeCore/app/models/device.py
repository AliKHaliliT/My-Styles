from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Device(Base, TimestampMixin):

    """

    Database representation of a connected client or tunnel profile.

    This model is protocol-agnostic. It stores a generic client identifier 
    and a JSON block for protocol-specific secrets (like private keys or 
    certificates), allowing the system to support multiple implementations.

    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_name: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Protocol Agnostic Fields
    client_identifier: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    protocol_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    
    status: Mapped[str] = mapped_column(
        String,
        CheckConstraint("status IN ('enabled', 'disabled')"),
        default="enabled",
        nullable=False,
    )

    user: Mapped[User] = relationship("User", back_populates="devices")
