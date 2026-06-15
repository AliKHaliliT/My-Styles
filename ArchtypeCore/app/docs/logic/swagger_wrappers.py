from typing import Any


def wrap_swagger_single_example(description: str, example_payload: dict[str, Any]) -> dict[str, Any]:

    """
    
    Wraps a single example payload in the format required by OpenAPI/Swagger.


    Parameters
    ----------
    description : str
        The text that appears next to the HTTP status code in the UI.

    example_payload : dict[str, Any]
        The actual JSON body.
        
        
    Returns
    -------
    swagger_dict : dict[str, Any]
        The heavily nested dictionary required by FastAPI's `responses` parameter.
    
    """

    if not isinstance(description, str):
        raise TypeError(f"description must be a string. Received: {description} with type {type(description)}")
    if not isinstance(example_payload, dict):
        raise TypeError(f"example_payload must be a dict. Received: {example_payload} with type {type(example_payload)}")
    

    return {
        "description": description,
        "content": {
            "application/json": {
                "example": example_payload
            }
        }
    }


def wrap_swagger_multi_examples(description: str, examples_dict: dict[str, dict[str, Any]]) -> dict[str, Any]:

    """
    
    Wraps multiple example payloads in the format required by OpenAPI/Swagger.


    Parameters
    ----------
    description : str
        The text that appears next to the HTTP status code in the UI.

    examples_dict : dict[str, dict[str, Any]]
        A dictionary mapping an example name to its summary and value.
        
        
    Returns
    -------
    swagger_dict : dict[str, Any]
        The heavily nested dictionary required by FastAPI's `responses` parameter.
    
    """

    if not isinstance(description, str):
        raise TypeError(f"description must be a string. Received: {description} with type {type(description)}")
    if not isinstance(examples_dict, dict):
        raise TypeError(f"examples_dict must be a dict. Received: {examples_dict} with type {type(examples_dict)}")
    

    return {
        "description": description,
        "content": {
            "application/json": {
                "examples": examples_dict
            }
        }
    }
