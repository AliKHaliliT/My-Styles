from fastapi import Depends

from app.api.v1.dependencies.core import get_settings
from app.core.config.settings import Settings
from app.core.security.local_auth import LocalAuthAdapter
from app.domain.interfaces.security import IAuthManager
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.interfaces.vpn import IVPNProvider
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from app.services.access import AuthService, DeviceService, UserService
from app.services.vpn.wireguard import WireGuardProvider

# --- Infrastructure Injection ---

def get_auth_manager() -> IAuthManager:

    """
    
    Get the authentication manager implementation.
    
    """

    return LocalAuthAdapter()


def get_vpn_provider(settings: Settings = Depends(get_settings)) -> IVPNProvider:

    """

    Get the VPN Provider implementation.
    
    """

    return WireGuardProvider(settings=settings)


def get_uow(auth_manager: IAuthManager = Depends(get_auth_manager)) -> IUnitOfWork:

    """

    Get the Unit Of Work implementation.
    
    """

    return SQLAlchemyUnitOfWork(auth_manager=auth_manager)


# --- Application Service Injection ---

def get_auth_service(
    uow: IUnitOfWork = Depends(get_uow),
    auth_manager: IAuthManager = Depends(get_auth_manager),
    settings: Settings = Depends(get_settings)
) -> AuthService:
    
    """

    Get the authentication service.
    
    """

    return AuthService(uow=uow, auth_manager=auth_manager, settings=settings)


def get_device_service(
    uow: IUnitOfWork = Depends(get_uow),
    vpn_provider: IVPNProvider = Depends(get_vpn_provider),
    settings: Settings = Depends(get_settings)
) -> DeviceService:
    
    """

    Get the device management service.
    
    """

    return DeviceService(
        uow=uow, vpn_provider=vpn_provider, settings=settings
    )


def get_user_service(
    uow: IUnitOfWork = Depends(get_uow),
    vpn_provider: IVPNProvider = Depends(get_vpn_provider),
) -> UserService:
    
    """

    Get the user management service.
    
    """

    return UserService(
        uow=uow, vpn_provider=vpn_provider
    )
