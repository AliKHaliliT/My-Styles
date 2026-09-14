from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


def generate_example_from_exception(exc: BaseException | type[BaseException]) -> dict[str, Any]:

    """

    Generates a dictionary example from an exception instance or a recognised class.

    This utility dynamically extracts all public attributes of an exception
    that do not begin with an underscore and are JSON-serializable, making
    it suitable for use in API documentation as a structured example.


    Parameters
    ----------
    exc : BaseException | type[BaseException]
        An exception instance to convert into an OpenAPI-compatible dictionary. The
        `RequestValidationError` class is accepted in place of an instance, because FastAPI
        builds it with a payload no caller can supply meaningfully here, so this function
        returns a hand-written example for it instead.

        
    Returns
    -------
    example : dict[str, Any]
        A dictionary containing serializable public attributes of the exception.


    Raises
    ------
    TypeError
        If the argument is not an exception class or instance.

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


    Raises
    ------
    TypeError
        If `Input` is not a Pydantic model class (subclass of BaseModel).

    """

    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise TypeError(
            f"Input must be a Pydantic model class (subclass of BaseModel). Received: {model} with type {type(model)}"
        )


    schema = model.model_json_schema()
    return _example_from_schema(schema.get("properties", {}), schema.get("$defs", {}))


_SCALAR_EXAMPLES: dict[str, Any] = {"string": "string", "integer": 1, "number": 1.0, "boolean": True}


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
            result[key] = _example_from_reference(val["$ref"], defs)
        else:
            result[key] = _placeholder_from_type(val, defs)


    return result


def _example_from_reference(ref: str, defs: dict[str, Any]) -> dict[str, Any]:

    """

    Generates the example of the schema a `$ref` points at, empty when the reference is unknown.

    """

    ref_key = ref.split("/")[-1]
    ref_schema = defs.get(ref_key, {})
    return _example_from_schema(ref_schema.get("properties", {}), defs)


def _placeholder_from_union(options: Any, defs: dict[str, Any]) -> Any:

    """

    Generates the example of the first usable member of an anyOf, oneOf, or allOf list.

    """

    if isinstance(options, list) and options:
        opt = options[0]
        if "$ref" in opt:
            return _example_from_reference(opt["$ref"], defs)
        elif "type" in opt or "properties" in opt:
            return _placeholder_from_type(opt, defs)
    return None


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
            return _placeholder_from_union(field[key], defs)

    t = field.get("type")
    if isinstance(t, str) and t in _SCALAR_EXAMPLES:
        return _SCALAR_EXAMPLES[t]

    if t == "array":
        item = field.get("items", {})
        if "$ref" in item:
            return [_example_from_reference(item["$ref"], defs)]
        else:
            return [_placeholder_from_type(item, defs)]

    if t == "object":
        return _example_from_schema(field.get("properties", {}), defs)

    if "$ref" in field:
        return _example_from_reference(field["$ref"], defs)

    return None
