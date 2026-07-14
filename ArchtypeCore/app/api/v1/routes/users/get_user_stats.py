from fastapi import Depends, Request

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas.users import UserStats
from app.api.v1.translators.users import domain_to_api_user_stats
from app.services.access.user_service import UserService


async def get_user_stats(
    request: Request,
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserStats:
    
    """

    Retrieves usage statistics for a specific user.

    """

    domain_stats = await user_service.get_user_stats(user_id=user_id)
    return domain_to_api_user_stats(domain_stats)
