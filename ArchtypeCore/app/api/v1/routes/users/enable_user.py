from fastapi import Depends, Request

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas.users import User
from app.api.v1.translators.users import domain_to_api_user
from app.services.access import UserService


async def enable_user(
    request: Request,
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> User:
    
    """

    Enables a previously disabled user.

    """

    domain_user = await user_service.enable_user(user_id=user_id)
    return domain_to_api_user(domain_user)
