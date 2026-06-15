from fastapi import status

from app.docs.logic import (build_standard_error_payload,
                            wrap_swagger_multi_examples)
from app.docs.v1.routers.common_docs import COMMON_RESPONSES

LOGIN_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: wrap_swagger_multi_examples(
        description="Unauthorized Error",
        examples_dict={
            "incorrect_credentials": {
                "summary": "Incorrect Credentials",
                "value": build_standard_error_payload(
                    title="HTTP Error 401",
                    detail="Incorrect username or password",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    error_type="http_error"
                )
            },
            "account_disabled": {
                "summary": "Account Disabled",
                "value": build_standard_error_payload(
                    title="HTTP Error 401",
                    detail="Account is disabled",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    error_type="http_error"
                )
            }
        }
    ),
    **COMMON_RESPONSES
}
