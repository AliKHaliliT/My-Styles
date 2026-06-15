from fastapi import Depends, HTTPException, Request, status

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

    try:
        domain_user = await user_service.enable_user(user_id=user_id)
        return domain_to_api_user(domain_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed: {e}")
