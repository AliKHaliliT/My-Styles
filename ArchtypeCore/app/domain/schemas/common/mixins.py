from pydantic import AwareDatetime, BaseModel


class IDMixin(BaseModel):

    """
    
    Adds an id field to a schema.
    
    """
    
    id: int


class TimeStampMixin(BaseModel):

    """
    
    Adds created_at and updated_at fields to a schema, each a moment that carries its offset.

    """

    created_at: AwareDatetime
    updated_at: AwareDatetime


class UserIDMixin(BaseModel):

    """
    
    Adds a user_id field to a schema.
    
    """
    
    user_id: int
