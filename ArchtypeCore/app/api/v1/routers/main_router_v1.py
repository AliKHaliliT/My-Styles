from fastapi import APIRouter

from app.api.v1.routers.auth_router import auth_router
from app.api.v1.routers.devices_router import devices_router
from app.api.v1.routers.users_router import users_router

v1 = APIRouter()


# Main
v1.include_router(auth_router)
v1.include_router(users_router)
v1.include_router(devices_router)
