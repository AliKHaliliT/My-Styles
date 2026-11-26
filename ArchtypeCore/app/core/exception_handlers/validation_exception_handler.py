from logging import getLogger

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
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


    Raises
    ------
    None.

    """

    logger.error(f"Validation error: {exc.errors()}")
    # A validator that refuses a value raises, and its error keeps the exception itself in its
    # context, which JSON cannot carry, so each exception is written as its message.
    errors = jsonable_encoder(exc.errors(), custom_encoder={Exception: str})


    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=build_standard_error_payload(
            title="Validation Error",
            detail=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_type="validation_error"
        )
    )
