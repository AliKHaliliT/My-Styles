from fastapi import Depends, HTTPException, Request, status

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas.users import User, UserCreate
from app.api.v1.translators.users import (api_to_domain_user_create,
                                          domain_to_api_user)
from app.services.access import UserService


async def add_user(
    request: Request,
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    
    """

    Adds a new user to the system.

    """

    try:
        domain_user_in = api_to_domain_user_create(user_in)
        domain_user = await user_service.create_user_with_device(user_in=domain_user_in)
        return domain_to_api_user(domain_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
