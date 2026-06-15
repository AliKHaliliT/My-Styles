from fastapi import APIRouter, status

from app.api.v1.routes.auth import admin_login
from app.api.v1.schemas.auth.auth_token import AuthToken
from app.docs.v1.routers.auth_docs import LOGIN_RESPONSES

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Admin Login
auth_router.add_api_route(
    "/login",
    admin_login,
    methods=["POST"],
    response_model=AuthToken,
    responses=LOGIN_RESPONSES,
    summary="Obtain an Access Token",
    response_description="Admin authentication successful.",
    status_code=status.HTTP_200_OK,
)
