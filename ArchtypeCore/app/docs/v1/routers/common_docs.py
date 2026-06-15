from fastapi import status
from fastapi.exceptions import RequestValidationError

from app.docs.logic import (build_standard_error_payload,
                            generate_example_from_exception,
                            wrap_swagger_multi_examples,
                            wrap_swagger_single_example)

# Standard Fallback Errors
VALIDATION_ERROR_RESPONSE = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: wrap_swagger_single_example(
        description="Validation Error",
        example_payload=generate_example_from_exception(RequestValidationError)
    )
}


INTERNAL_SERVER_ERROR_RESPONSE = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: wrap_swagger_single_example(
        description="Internal Server Error",
        example_payload=build_standard_error_payload(
            title="Internal Server Error",
            detail="An unexpected error occurred during processing.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type="unhandled_server_error"
        )
    )
}


COMMON_RESPONSES = {
    **VALIDATION_ERROR_RESPONSE,
    **INTERNAL_SERVER_ERROR_RESPONSE
}


# Security Errors (Applied to endpoints protected by dependencies)
SECURITY_RESPONSES = {
    status.HTTP_403_FORBIDDEN: wrap_swagger_multi_examples(
        description="Forbidden Error",
        examples_dict={
            "invalid_token": {
                "summary": "Invalid or Missing Token",
                "value": build_standard_error_payload(
                    title="HTTP Error 403",
                    detail="Could not validate credentials",
                    status_code=status.HTTP_403_FORBIDDEN,
                    error_type="http_error"
                )
            },
            "inactive_account": {
                "summary": "Inactive Account",
                "value": build_standard_error_payload(
                    title="HTTP Error 403",
                    detail="Inactive admin account",
                    status_code=status.HTTP_403_FORBIDDEN,
                    error_type="http_error"
                )
            }
        }
    )
}


STANDARD_ROUTER_RESPONSES = {
    **COMMON_RESPONSES,
    **SECURITY_RESPONSES
}
