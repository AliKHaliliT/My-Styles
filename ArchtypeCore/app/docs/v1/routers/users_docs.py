from typing import Any

from fastapi import status

from app.docs.logic import (build_standard_error_payload,
                            wrap_swagger_multi_examples,
                            wrap_swagger_single_example)
from app.docs.v1.routers.common_docs import STANDARD_ROUTER_RESPONSES

ADD_USER_RESPONSES: dict[int | str, dict[str, Any]] = {
    status.HTTP_409_CONFLICT: wrap_swagger_single_example(
        description="Conflict",
        example_payload=build_standard_error_payload(
            title="Conflict",
            detail="User with username '{username}' already exists",
            status_code=status.HTTP_409_CONFLICT,
            error_type="conflict"
        )
    ),
    **STANDARD_ROUTER_RESPONSES
}


USER_ACTION_RESPONSES: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: wrap_swagger_single_example(
        description="User Not Found",
        example_payload=build_standard_error_payload(
            title="Not Found",
            detail="User with ID {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_type="not_found"
        )
    ),
    **STANDARD_ROUTER_RESPONSES
}


GET_USER_CONFIG_RESPONSES: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: wrap_swagger_multi_examples(
        description="Not Found Error",
        examples_dict={
            "device_not_found": {
                "summary": "Device Not Found",
                "value": build_standard_error_payload(
                    title="Not Found",
                    detail="Device not found for this user",
                    status_code=status.HTTP_404_NOT_FOUND,
                    error_type="not_found"
                )
            },
            "user_not_found": {
                "summary": "User Not Found",
                "value": build_standard_error_payload(
                    title="Not Found",
                    detail="User with ID {id} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                    error_type="not_found"
                )
            }
        }
    ),
    **STANDARD_ROUTER_RESPONSES
}


LIST_USERS_RESPONSES: dict[int | str, dict[str, Any]] = {
    **STANDARD_ROUTER_RESPONSES
}
