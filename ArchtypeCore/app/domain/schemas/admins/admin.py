from pydantic import BaseModel

from app.domain.schemas.common import IDMixin


class AdminBase(BaseModel):

    """
    
    Base Domain schema shared across admin variants.
    
    """

    username: str


class AdminCreate(AdminBase):

    """
    
    Domain schema used when creating a new admin.
    
    """

    password: str
    role: str = "admin"
    status: str = "enabled"


class AdminInDB(IDMixin, AdminBase):

    """
    
    Domain schema representing how an admin is stored in the database.
    
    """

    hashed_password: str
    role: str
    status: str

    class Config:
        from_attributes = True


class Admin(AdminBase):
    
    """
    
    Domain schema representing an admin.
    
    """

    ...


class AdminUpdate(AdminBase):

    """
    
    Domain schema used for partial updates to an admin.
    
    """
    
    username: str | None = None
    password: str | None = None
    role: str | None = None
    status: str | None = None
