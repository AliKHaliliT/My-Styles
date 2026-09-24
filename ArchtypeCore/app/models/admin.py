from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.mixins import TimestampMixin


class Admin(Base, TimestampMixin):

    """

    Database representation of an administrative user.

    This model stores credentials and role information for users who have
    access to the management plane of ArchetypeCore.

    """

    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, server_default="admin")
    status: Mapped[str] = mapped_column(String, nullable=False, server_default="enabled")
