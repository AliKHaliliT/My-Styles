from app.domain.schemas.admins import AdminInDB as DomainAdminInDB
from app.models.admin import Admin as DBAdmin


def db_to_domain_admin_in_db(db_admin: DBAdmin) -> DomainAdminInDB:

    """

    Convert Database Admin to Domain AdminInDB.

    """

    return DomainAdminInDB.model_validate(db_admin, from_attributes=True)
