from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


def generate_example_from_exception(exc: BaseException) -> dict[str, Any]:

    """

    Generates a dictionary example from any exception instance.

    This utility dynamically extracts all public attributes of an exception 
    that do not begin with an underscore and are JSON-serializable, making 
    it suitable for use in API documentation as a structured example.

    
    Parameters
    ----------
    exc : BaseException
        Any exception instance to convert into an OpenAPI-compatible dictionary.

        
    Returns
    -------
    example : dict[str, Any]
        A dictionary containing serializable public attributes of the exception.

    """

    # Special case for FastAPI's RequestValidationError
    if exc == RequestValidationError:
        return {
            "title": "Validation Error",
            "detail": [
                {
                    "loc": ["body", "field_name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": "bad_value"
                }
            ],
            "status_code": 422,
            "type": "validation_error"
        }

    if not isinstance(exc, BaseException):
        raise TypeError(f"Expected an exception instance. Received: {exc} with type {type(exc)}")


    example = {}
    for attr in dir(exc):
        if attr.startswith("_"):
            continue
        value = getattr(exc, attr)
        if callable(value):
            continue
        if attr == "args":
            continue
        try:
            import json
            json.dumps(value)
            example[attr] = value
        except (TypeError, ValueError):
            continue


    return example


def generate_example_from_pydantic(model: type[BaseModel]) -> dict[str, Any]:

    """

    Generates a Swagger-style example dictionary from a Pydantic model.

    This function analyzes the JSON schema of a Pydantic model and produces an
    example dictionary that conforms to the model's structure and types. It 
    supports nested models, arrays, and unions (anyOf, oneOf, allOf).


    Parameters
    ----------
    model : type[BaseModel]
        The Pydantic model class to generate the example from.

        
    Returns
    -------
    example : dict[str, Any]
        A dictionary containing example values matching the model's schema.

    """

    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise TypeError(
            f"Input must be a Pydantic model class (subclass of BaseModel). Received: {model} with type {type(model)}"
        )
    

    def _example_from_schema(props: dict[str, Any], defs: dict[str, Any]) -> dict[str, Any]:

        """

        Recursively generates example values for a given set of schema properties.

        """

        if not isinstance(props, dict):
            raise TypeError(f"props must be a dictionary. Received: {props} with type {type(props)}")
        if not isinstance(defs, dict):
            raise TypeError(f"defs must be a dictionary. Received: {defs} with type {type(defs)}")


        result = {}
        for key, val in props.items():
            if "$ref" in val:
                ref_key = val["$ref"].split("/")[-1]
                ref_schema = defs.get(ref_key, {})
                result[key] = _example_from_schema(ref_schema.get("properties", {}), defs)
            else:
                result[key] = _placeholder_from_type(val, defs)


        return result


    def _placeholder_from_type(field: dict[str, Any], defs: dict[str, Any]) -> Any:

        """

        Generates a placeholder example value for a field based on its type.

        """

        if not isinstance(field, dict):
            raise TypeError(f"field must be a dictionary. Received: {field} with type {type(field)}")
        if not isinstance(defs, dict):
            raise TypeError(f"defs must be a dictionary. Received: {defs} with type {type(defs)}")
        

        for key in ("anyOf", "oneOf", "allOf"):
            if key in field:
                options = field[key]
                if isinstance(options, list) and options:
                    opt = options[0]
                    if "$ref" in opt:
                        ref_key = opt["$ref"].split("/")[-1]
                        ref_schema = defs.get(ref_key, {})
                        return _example_from_schema(ref_schema.get("properties", {}), defs)
                    elif "type" in opt or "properties" in opt:
                        return _placeholder_from_type(opt, defs)
                return None

        t = field.get("type")
        if t == "string":
            return "string"
        if t == "integer":
            return 1
        if t == "number":
            return 1.0
        if t == "boolean":
            return True

        if t == "array":
            item = field.get("items", {})
            if "$ref" in item:
                ref_key = item["$ref"].split("/")[-1]
                item_schema = defs.get(ref_key, {})
                return [_example_from_schema(item_schema.get("properties", {}), defs)]
            else:
                return [_placeholder_from_type(item, defs)]

        if t == "object":
            return _example_from_schema(field.get("properties", {}), defs)

        if "$ref" in field:
            ref_key = field["$ref"].split("/")[-1]
            ref_schema = defs.get(ref_key, {})
            return _example_from_schema(ref_schema.get("properties", {}), defs)

        return None


    schema = model.model_json_schema()
    return _example_from_schema(schema.get("properties", {}), schema.get("$defs", {}))
