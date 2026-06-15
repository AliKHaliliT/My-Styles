from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.docs.logic import build_standard_error_payload
from app.domain.exceptions import AuthenticationError, EntityNotFoundError

logger = getLogger(__name__)


async def domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    """

    Handler for domain-specific exceptions to map them to HTTP responses.

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : Exception
        The Domain Exception instance caught.

        
    Returns
    -------
    JSONResponse
        A JSON response detailing the domain error.

    """

    logger.warning(f"Domain exception: {exc}")


    headers = None

    if isinstance(exc, AuthenticationError):
        status_code = status.HTTP_401_UNAUTHORIZED
        title = "Authentication Failed"
        error_type = "unauthorized"
        headers = {"WWW-Authenticate": "Bearer"}
    elif isinstance(exc, EntityNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
        title = "Not Found"
        error_type = "not_found"
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        title = "Bad Request"
        error_type = "bad_request"


    return JSONResponse(
        status_code=status_code,
        content=build_standard_error_payload(
            title=title,
            detail=str(exc),
            status_code=status_code,
            error_type=error_type
        ),
        headers=headers
    )
