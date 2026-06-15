from typing import Any


def build_standard_error_payload(
    title: str, 
    detail: Any, 
    status_code: int, 
    error_type: str | None = None
) -> dict[str, Any]:

    """
    
    Constructs the standard JSON shape for all API errors.


    Parameters
    ----------
    title : str
        Message title.

    detail : Any
        Message detail. Can be a string, or a generated dictionary from Pydantic/Exceptions.

    status_code : int
        The HTTP Status code.

    error_type : str | None, optional
        A machine-readable error classification. The default value is `None`.
        
        
    Returns
    -------
    payload : dict[str, Any]
        A dictionary formatted exactly how the API will return it to the client.
    
    """

    if not isinstance(title, str):
        raise TypeError(f"title must be a string. Received: {title} with type {type(title)}")
    if not isinstance(status_code, int):
        raise TypeError(f"status_code must be an integer. Received: {status_code} with type {type(status_code)}")
    if error_type is not None and not isinstance(error_type, str):
        raise TypeError(f"error_type must be a string. Received: {error_type} with type {type(error_type)}")


    return {
        "title": title,
        "detail": detail,
        "status_code": status_code,
        "type": error_type or "error"
    }
