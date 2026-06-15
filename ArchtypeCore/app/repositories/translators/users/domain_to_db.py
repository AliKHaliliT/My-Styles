from typing import Any

from app.domain.schemas.users import UserCreate as DomainUserCreate
from app.domain.schemas.users import UserUpdate as DomainUserUpdate
from app.models.user import User as DBUser


def domain_to_db_user_create(domain_obj: DomainUserCreate) -> DBUser:

    """

    Convert Domain UserCreate to a new Database User model.

    """

    return DBUser(
        username=domain_obj.username,
        quota_bytes=domain_obj.quota_bytes
    )


def domain_to_db_user_update(domain_obj: DomainUserUpdate) -> dict[str, Any]:

    """

    Convert Domain UserUpdate to a dictionary of Database columns, dropping None values.

    """

    update_data = {}
    
    if domain_obj.username is not None:
        update_data["username"] = domain_obj.username
    if domain_obj.quota_bytes is not None:
        update_data["quota_bytes"] = domain_obj.quota_bytes
    if domain_obj.used_bytes is not None:
        update_data["used_bytes"] = domain_obj.used_bytes
    if domain_obj.status is not None:
        update_data["status"] = domain_obj.status
        
    return update_data
