from sqlalchemy import Column, DateTime, func


class TimestampMixin:

    """
    
    Adds created_at and updated_at timestamps to a model.
    
    """
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
