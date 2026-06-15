from datetime import datetime

from pydantic import BaseModel


class IDMixin(BaseModel):

    """
    
    Adds an id field to a schema.
    
    """
    
    id: int


class TimeStampMixin(BaseModel):

    """
    
    Adds created_at and updated_at fields to a schema.
    
    """

    created_at: datetime
    updated_at: datetime


class UserIDMixin(BaseModel):

    """
    
    Adds a user_id field to a schema.
    
    """
    
    user_id: int
