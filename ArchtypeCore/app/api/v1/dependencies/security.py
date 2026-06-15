from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.dependencies.services import get_auth_manager, get_uow
from app.domain.interfaces.security import IAuthManager
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.schemas.admins import AdminInDB


def get_reusable_oauth2() -> OAuth2PasswordBearer:

    """
    
    Get reusable OAuth2PasswordBearer instance for token extraction.
    
    """

    return OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_admin(
    token: str = Depends(get_reusable_oauth2()),
    auth_manager: IAuthManager = Depends(get_auth_manager),
    uow: IUnitOfWork = Depends(get_uow),
) -> AdminInDB:
    
    """
    
    Get current admin from valid JWT token.
    
    """

    payload = auth_manager.decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token payload"
        )

    async with uow:
        admin_domain = await uow.admins.get_by_username(username=username)

    if not admin_domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    return admin_domain


async def get_current_active_admin(
    current_admin: AdminInDB = Depends(get_current_admin),
) -> AdminInDB:
    
    """
    
    Get current active admin.
    
    """
    
    if getattr(current_admin, "status", "enabled") != "enabled":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive admin account"
        )
    
    return current_admin
