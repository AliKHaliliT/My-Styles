from app.api.v1.dependencies.core import get_settings
from app.api.v1.dependencies.security import (get_current_active_admin,
                                              get_current_admin,
                                              get_reusable_oauth2)
from app.api.v1.dependencies.services import (get_auth_manager,
                                              get_auth_service,
                                              get_device_service, get_uow,
                                              get_user_service,
                                              get_vpn_provider)
