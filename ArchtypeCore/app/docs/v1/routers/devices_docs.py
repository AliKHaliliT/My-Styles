from fastapi import status

from app.docs.logic import (build_standard_error_payload,
                            wrap_swagger_single_example)
from app.docs.v1.routers.common_docs import STANDARD_ROUTER_RESPONSES

ADD_DEVICE_RESPONSES = {
    status.HTTP_404_NOT_FOUND: wrap_swagger_single_example(
        description="User Not Found",
        example_payload=build_standard_error_payload(
            title="HTTP Error 404",
            detail="User with ID {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_type="http_error"
        )
    ),
    **STANDARD_ROUTER_RESPONSES
}


DEVICE_ACTION_RESPONSES = {
    status.HTTP_404_NOT_FOUND: wrap_swagger_single_example(
        description="Device Not Found",
        example_payload=build_standard_error_payload(
            title="HTTP Error 404",
            detail="Device with ID {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_type="http_error"
        )
    ),
    **STANDARD_ROUTER_RESPONSES
}
