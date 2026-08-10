from typing import Any

from keel.domain.schemas.runs import RunState
from keel.domain.schemas.tools import ToolSpec


def domain_to_provider_tools(specs: list[ToolSpec]) -> list[dict[str, Any]]:

    """

    Convert Domain ToolSpecs to provider tool declarations.

    """

    return [
        {
            "function_declarations": [
                {
                    "name": spec.name,
                    "description": spec.description,
                    "parameters_json_schema": spec.parameters or {"type": "object", "properties": {}},
                }
                for spec in specs
            ]
        }
    ]


def domain_to_provider_contents(state: RunState) -> list[dict[str, Any]]:

    """

    Convert a Domain RunState transcript to a provider content history.

    """

    contents: list[dict[str, Any]] = [{"role": "user", "parts": [{"text": state.goal}]}]

    for step in state.transcript:
        if step.action.kind != "tool_call" or step.result is None:
            continue

        contents.append({
            "role": "model",
            "parts": [
                {
                    "function_call": {
                        "name": step.action.tool_name,
                        "args": step.action.arguments,
                    }
                }
            ],
        })
        contents.append({
            "role": "user",
            "parts": [
                {
                    "function_response": {
                        "name": step.action.tool_name,
                        "response": {
                            "content": step.result.content,
                            "is_error": step.result.is_error,
                        },
                    }
                }
            ],
        })

    return contents
