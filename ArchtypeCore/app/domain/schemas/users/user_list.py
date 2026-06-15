from pydantic import BaseModel

from app.domain.schemas.users.user import User


class UserListBase(BaseModel):

    """

    Base Domain schema shared across user list variants.

    """

    users: list[User]


class UserList(UserListBase):

    """

    Domain schema representing a user list.

    """
    
    pass
