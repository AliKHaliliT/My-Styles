from fastapi import Depends, Request

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas.users import UserList
from app.api.v1.translators.users import domain_to_api_user_list
from app.services.access.user_service import UserService


async def list_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> UserList:
    
    """

    Retrieves a paginated list of all users in the system.

    """

    domain_users = await user_service.get_all_users(skip=skip, limit=limit)
    return domain_to_api_user_list(domain_users)
