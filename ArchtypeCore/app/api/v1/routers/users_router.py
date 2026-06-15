from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_current_active_admin
from app.api.v1.routes.users import (add_user, disable_user, enable_user,
                                     get_user_config, get_user_stats,
                                     list_users)
from app.api.v1.schemas.devices.device_config import DeviceConfig
from app.api.v1.schemas.users import User, UserList, UserStats
from app.docs.v1.routers.users_docs import (ADD_USER_RESPONSES,
                                            GET_USER_CONFIG_RESPONSES,
                                            LIST_USERS_RESPONSES,
                                            USER_ACTION_RESPONSES)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_active_admin)]
)

# User Creation
users_router.add_api_route(
    "/add_user",
    add_user,
    methods=["POST"],
    response_model=User,
    responses=ADD_USER_RESPONSES,
    summary="Create a New User",
    response_description="The user was created successfully.",
    status_code=status.HTTP_201_CREATED,
)


# Disable User
users_router.add_api_route(
    "/{user_id}/disable",
    disable_user,
    methods=["POST"],
    response_model=User,
    responses=USER_ACTION_RESPONSES,
    summary="Disable a User",
    response_description="The specified user disabled successfully.",
    status_code=status.HTTP_200_OK,
)


# Enable User
users_router.add_api_route(
    "/{user_id}/enable",
    enable_user,
    methods=["POST"],
    response_model=User,
    responses=USER_ACTION_RESPONSES,
    summary="Enable a User",
    response_description="The specified user enabled successfully.",
    status_code=status.HTTP_200_OK,
)


# Device Configuration
users_router.add_api_route(
    "/{user_id}/devices/{device_id}/config",
    get_user_config,
    methods=["GET"],
    response_model=DeviceConfig,
    responses=GET_USER_CONFIG_RESPONSES,
    summary="Get User's Device Configuration",
    response_description="Client configuration for the specified user and device retrieved successfully.",
    status_code=status.HTTP_200_OK,
)


# User Statistics
users_router.add_api_route(
    "/{user_id}/stats",
    get_user_stats,
    methods=["GET"],
    response_model=UserStats,
    responses=USER_ACTION_RESPONSES,
    summary="Get User Statistics",
    response_description="Statistics for the specified user retrieved successfully.",
    status_code=status.HTTP_200_OK,
)


# List Users
users_router.add_api_route(
    "/list_users",
    list_users,
    methods=["GET"],
    response_model=UserList,
    responses=LIST_USERS_RESPONSES,
    summary="List All Users",
    response_description="The list of users retrieved successfully.",
    status_code=status.HTTP_200_OK,
)
