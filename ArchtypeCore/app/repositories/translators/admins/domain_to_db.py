from typing import Any

from app.domain.schemas.admins import AdminCreate as DomainAdminCreate
from app.domain.schemas.admins import AdminUpdate as DomainAdminUpdate
from app.models.admin import Admin as DBAdmin


def domain_to_db_admin_create(domain_obj: DomainAdminCreate, hashed_password: str) -> DBAdmin:

    """

    Convert Domain AdminCreate to a new Database Admin model.

    """

    return DBAdmin(
        username=domain_obj.username,
        hashed_password=hashed_password,
        role=domain_obj.role,
        status=domain_obj.status
    )


def domain_to_db_admin_update(domain_obj: DomainAdminUpdate, hashed_password: str | None = None) -> dict[str, Any]:

    """

    Convert Domain AdminUpdate to a dictionary of Database columns, dropping None values.

    """

    update_data = {}
    
    if domain_obj.username is not None:
        update_data["username"] = domain_obj.username
    if hashed_password is not None:
        update_data["hashed_password"] = hashed_password
    if domain_obj.role is not None:
        update_data["role"] = domain_obj.role
    if domain_obj.status is not None:
        update_data["status"] = domain_obj.status
        
    return update_data
