from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.types import UTCDateTime


class TimestampMixin:

    """
    
    Adds created_at and updated_at timestamps to a model, each handed back aware and in UTC.
    
    """
    
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False, server_default=func.now(), onupdate=func.now())
