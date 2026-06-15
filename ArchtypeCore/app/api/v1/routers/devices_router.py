from fastapi import APIRouter, Depends
from starlette import status

from app.api.v1.dependencies import get_current_active_admin
from app.api.v1.routes.devices import (add_device, disable_device,
                                       enable_device, get_device_config)
from app.api.v1.schemas.devices import Device
from app.api.v1.schemas.devices.device_config import DeviceConfig
from app.docs.v1.routers.devices_docs import (ADD_DEVICE_RESPONSES,
                                              DEVICE_ACTION_RESPONSES)

devices_router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
    dependencies=[Depends(get_current_active_admin)]
)

# Add Device
devices_router.add_api_route(
    "/add_device",
    add_device,
    methods=["POST"],
    response_model=Device,
    responses=ADD_DEVICE_RESPONSES,
    summary="Add a New Device to a User",
    response_description="The device was created and added to the user successfully.",
    status_code=status.HTTP_201_CREATED
)


# Disable Device
devices_router.add_api_route(
    "/{device_id}/disable",
    disable_device,
    methods=["POST"],
    response_model=Device,
    responses=DEVICE_ACTION_RESPONSES,
    summary="Disable a Device",
    response_description="The specified device disabled successfully.",
    status_code=status.HTTP_200_OK,
)


# Enable Device
devices_router.add_api_route(
    "/{device_id}/enable",
    enable_device,
    methods=["POST"],
    response_model=Device,
    responses=DEVICE_ACTION_RESPONSES,
    summary="Enable a Device",
    response_description="The specified device enabled successfully.",
    status_code=status.HTTP_200_OK,
)


# Get Device Config
devices_router.add_api_route(
    "/{device_id}/config",
    get_device_config,
    methods=["GET"],
    response_model=DeviceConfig,
    responses=DEVICE_ACTION_RESPONSES,
    summary="Get Device Configuration",
    response_description="Client configuration for the specified device retrieved successfully.",
    status_code=status.HTTP_200_OK,
)
