from logging import getLogger

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.docs.logic import build_standard_error_payload

logger = getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:

    """

    Handler for standard FastAPI HTTPExceptions not caught by custom exceptions.

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : HTTPException
        The HTTP Exception instance caught.

        
    Returns
    -------
    JSONResponse
        A JSON response detailing the HTTP error.

    """

    logger.error(f"HTTP Exception: {exc.status_code}: {exc.detail}")


    return JSONResponse(
        status_code=exc.status_code,
        content=build_standard_error_payload(
            title=f"HTTP Error {exc.status_code}",
            detail=exc.detail,
            status_code=exc.status_code,
            error_type="http_error"
        ),
        headers=exc.headers
    )
