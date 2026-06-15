from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.routers.main_router_v1 import v1
from app.core.config.settings import settings
from app.core.exception_handlers import (domain_exception_handler,
                                         general_exception_handler,
                                         http_exception_handler,
                                         validation_exception_handler)
from app.core.exceptions import CustomHTTPException
from app.core.logging.logging_config import setup_logging
from app.core.middlewares.cache import NoCacheMiddleware
from app.core.middlewares.isolation import (
    CrossOriginEmbedderPolicyMiddleware, CrossOriginOpenerPolicyMiddleware,
    CrossOriginResourcePolicyMiddleware, OriginAgentClusterMiddleware)
from app.core.middlewares.observability import (AccessLogMiddleware,
                                                RequestIDMiddleware)
from app.core.middlewares.security import (ContentSecurityPolicyMiddleware,
                                           PermissionsPolicyMiddleware,
                                           ReferrerPolicyMiddleware,
                                           StrictTransportSecurityMiddleware,
                                           XContentTypeOptionsMiddleware,
                                           XDNSPrefetchControlMiddleware,
                                           XDownloadOptionsMiddleware,
                                           XFrameOptionsMiddleware,
                                           XXSSProtectionMiddleware)
from app.domain.exceptions import DomainException


# Startup Events
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Configure Logging
    setup_logging(handler_log_level=settings.HANDLER_LOG_LEVEL, 
                  root_log_level=settings.ROOT_LOG_LEVEL, 
                  uvicorn_log_level=settings.UVICORN_LOG_LEVEL)


    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_PREFIX}{settings.DOCS_URL}",
    redoc_url=f"{settings.API_V1_PREFIX}{settings.REDOC_URL}",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)


# Configure Exception Handlers
## Custom Default Handlers 
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomHTTPException, http_exception_handler)
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Configure Middlewares
## Custom Access Logging
### Must come before the Request ID Middleware
app.add_middleware(AccessLogMiddleware)

## Request ID
app.add_middleware(RequestIDMiddleware)

## CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS
)

## Other Security Middlewares
app.add_middleware(StrictTransportSecurityMiddleware)
app.add_middleware(XContentTypeOptionsMiddleware)
### For demonstration purposes, security settings have been relaxed to make publishing and viewing the auto-generated documentation easier.
### In a real enterprise project, you should enforce stricter policies—avoid practices like "unsafe-inline" and instead use safer alternatives such as nonce.
### Additionally, the frontend here uses a development build of Tailwind. 
### In an enterprise environment, this should be properly optimized and prepared for production.
app.add_middleware(
    ContentSecurityPolicyMiddleware,
    policy=(
        "default-src 'self'; "
        
        # Scripts
        "script-src 'self'; "
        "script-src-elem 'self' "
        "https://cdn.tailwindcss.com "
        "https://cdn.jsdelivr.net "
        "https://cdnjs.cloudflare.com "
        "https://unpkg.com "
        "'unsafe-inline'; "
        
        # Workers
        "worker-src 'self' blob: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        
        # Styles
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
        "style-src-elem 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net 'unsafe-inline'; "
        
        # Fonts
        "font-src https://fonts.gstatic.com; "
        
        # Images
        "img-src 'self' data: "
        "https://fastapi.tiangolo.com "
        "https://cdn.redoc.ly "
        "https://cdn.jsdelivr.net; "
        
        # Misc
        "object-src 'none'; "
        "frame-ancestors 'none';"
    )
)
app.add_middleware(PermissionsPolicyMiddleware)
# app.add_middleware(CrossOriginOpenerPolicyMiddleware)
# app.add_middleware(CrossOriginEmbedderPolicyMiddleware)
app.add_middleware(CrossOriginResourcePolicyMiddleware)
app.add_middleware(ReferrerPolicyMiddleware)
app.add_middleware(XFrameOptionsMiddleware)
app.add_middleware(XXSSProtectionMiddleware, policy="1; mode=block")
app.add_middleware(XDownloadOptionsMiddleware)
app.add_middleware(OriginAgentClusterMiddleware)
app.add_middleware(NoCacheMiddleware)
app.add_middleware(XDNSPrefetchControlMiddleware)


# APIs
## v1
app.include_router(v1, prefix=settings.API_V1_PREFIX)

## Root
@app.get("/")
async def root(request: Request):
    return JSONResponse(status_code=200, content={"message": "This is the root endpoint."})

## Health Check
@app.get("/health")
async def health(request: Request):
    return JSONResponse(status_code=200, content={"message": "Server is UP AND RUNNING!"})
