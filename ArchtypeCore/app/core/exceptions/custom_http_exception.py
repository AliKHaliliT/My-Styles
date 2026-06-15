from typing import Any

from fastapi import HTTPException


class CustomHTTPException(HTTPException):

    """

    Base exception for the Application API.

    
    Usage
    -----
    ```python
    from app.core.exceptions import CustomHTTPException

    raise CustomHTTPException(
        status_code=500,
        detail="Internal server error",
        headers={"X-Error-Type": "api_error"}
    )
    ```
    
    """

    def __init__(
        self,
        status_code: int = 500,
        detail: str | dict[str, Any] | list[Any] = "An unexpected error occurred during processing.",
        headers: dict[str, str] | None = None,
        title: str | None = "Internal Server Error",
        error_type: str | None = None
    ) -> None:
        
        """

        Constructor for the Custom HTTP Exception.

        
        Parameters
        ----------
        status_code : int, optional
            HTTP status code for the exception. The default value is `500`.

        detail : str | dict[str, Any] | list[Any], optional
            Detailed error message or object. The default value is `"Internal server error"`.

        headers : dict[str, str] | None, optional
            Headers to include in the HTTP response. The default value is `None`.

        title : str | None, optional
            Title of the error. The default value is `None`. If `None`, defaults to `"Error"`.

        error_type : str | None, optional
            Type of the error, The default value is `None`. If `None`, defaults to `"api_error"`.

            
        Returns
        -------
        None.

        """

        super().__init__(status_code=status_code, detail=detail, headers=headers)

        self.title = title or "Error"
        self.error_type = error_type or "api_error"
