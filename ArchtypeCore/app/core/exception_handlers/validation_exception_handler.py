from logging import getLogger

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.docs.logic import build_standard_error_payload

logger = getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:

    """

    Handler for request validation errors (e.g., Pydantic errors).

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : RequestValidationError
        The Request Validation Error instance caught.

        
    Returns
    -------
    JSONResponse
        A JSON response detailing the validation error.

    """

    logger.error(f"Validation error: {exc.errors()}")


    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_standard_error_payload(
            title="Validation Error",
            detail=exc.errors(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_type="validation_error"
        )
    )
