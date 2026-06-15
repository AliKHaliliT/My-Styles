from sqlalchemy import Column, Integer, String

from db.base import Base
from db.mixins import TimestampMixin


class Admin(Base, TimestampMixin):

    """

    Database representation of an administrative user.

    This model stores credentials and role information for users who have
    access to the management plane of ArchetypeCore.

    """

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="admin")
    status = Column(String, nullable=False, server_default="enabled")
