from app.domain.schemas.users import User as DomainUser
from app.models.user import User as DBUser


def db_to_domain_user(db_user: DBUser) -> DomainUser:

    """

    Convert Database User to Domain User.

    """

    return DomainUser.model_validate(db_user, from_attributes=True)
