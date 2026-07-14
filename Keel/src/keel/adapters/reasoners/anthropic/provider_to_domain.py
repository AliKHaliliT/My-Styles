from typing import Any

from keel.domain.exceptions import ReasoningError
from keel.domain.schemas.actions import Action, Finish, ToolCall


def provider_to_domain_action(response: Any) -> Action:

    """
    
    Convert a provider message response to a Domain Action.
    
    """

    if getattr(response, "stop_reason", None) == "refusal":
        raise ReasoningError("The provider declined to process the request")

    for block in response.content:
        if block.type == "tool_use":
            return ToolCall(tool_name=block.name, arguments=dict(block.input))

    text = "".join(block.text for block in response.content if block.type == "text").strip()
    if not text:
        raise ReasoningError("The provider returned neither a tool call nor a textual conclusion")

    return Finish(output=text)
