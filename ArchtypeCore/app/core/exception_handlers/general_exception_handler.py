from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.docs.logic import build_standard_error_payload

logger = getLogger(__name__)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    """

    Handler for all other unhandled exceptions.

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : Exception
        The unhandled Exception instance caught.

        
    Returns
    -------
    JSONResponse
        A JSON response detailing the internal server error.

    """

    logger.exception(f"Unhandled exception: {exc}")


    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_standard_error_payload(
            title="Internal Server Error",
            detail="An unexpected error occurred during processing.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type="unhandled_server_error"
        )
    )
