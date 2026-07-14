from typing import Any

from keel.domain.schemas.runs import RunState
from keel.domain.schemas.tools import ToolSpec


def domain_to_provider_tools(specs: list[ToolSpec]) -> list[dict[str, Any]]:

    """
    
    Convert Domain ToolSpecs to provider tool definitions.
    
    """

    return [
        {
            "name": spec.name,
            "description": spec.description,
            "input_schema": spec.parameters or {"type": "object", "properties": {}},
        }
        for spec in specs
    ]


def domain_to_provider_messages(state: RunState) -> list[dict[str, Any]]:

    """
    
    Convert a Domain RunState transcript to a provider message history.
    
    """

    messages: list[dict[str, Any]] = [{"role": "user", "content": state.goal}]

    for step in state.transcript:
        if step.action.kind != "tool_call" or step.result is None:
            continue

        tool_use_id = f"toolu_step_{step.index}"
        messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": tool_use_id,
                    "name": step.action.tool_name,
                    "input": step.action.arguments,
                }
            ],
        })
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": step.result.content,
                    "is_error": step.result.is_error,
                }
            ],
        })

    return messages
