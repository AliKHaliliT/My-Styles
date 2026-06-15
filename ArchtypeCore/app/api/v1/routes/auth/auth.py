from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import get_auth_service
from app.api.v1.schemas.auth import AuthToken
from app.api.v1.translators.auth import domain_to_api_auth_token
from app.services.access import AuthService


async def admin_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> AuthToken:
    
    """

    Authenticates an admin user.

    """

    domain_token = await auth_service.authenticate_admin(
        username=form_data.username,
        password=form_data.password
    )

    return domain_to_api_auth_token(domain_token)
