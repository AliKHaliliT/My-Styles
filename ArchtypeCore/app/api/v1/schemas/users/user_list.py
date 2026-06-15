from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.users.user import User


class UserListBase(BaseModel):

    """

    Base API schema shared across user list variants.

    """

    users: list[User]


class UserList(UserListBase):

    """

    API schema representing a user list.

    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "quota_bytes": 10737418240,
                        "status": "enabled",
                        "used_bytes": 536870912,
                        "devices": [],
                        "created_at": "2026-06-15T12:00:00Z",
                        "updated_at": "2026-06-15T12:00:00Z"
                    }
                ]
            }
        }
    )
