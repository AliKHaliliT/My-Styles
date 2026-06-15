from app.api.v1.schemas.users import UserCreate as APIUserCreate
from app.domain.schemas.users import UserCreate as DomainUserCreate


def api_to_domain_user_create(api_in: APIUserCreate) -> DomainUserCreate:

    """

    Convert API UserCreate to Domain UserCreate.

    """
    
    return DomainUserCreate(**api_in.model_dump())
