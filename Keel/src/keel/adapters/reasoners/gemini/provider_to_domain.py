from typing import Any

from keel.domain.exceptions import ReasoningError
from keel.domain.schemas.actions import Action, Finish, ToolCall


def provider_to_domain_action(response: Any) -> Action:

    """

    Convert a provider generate-content response to a Domain Action.

    """

    feedback = getattr(response, "prompt_feedback", None)
    if feedback is not None and getattr(feedback, "block_reason", None):
        raise ReasoningError("The provider declined to process the request")

    candidates = getattr(response, "candidates", None) or []
    parts: list[Any] = []
    if candidates:
        content = getattr(candidates[0], "content", None)
        parts = getattr(content, "parts", None) or []

    for part in parts:
        call = getattr(part, "function_call", None)
        if call is not None and getattr(call, "name", None):
            return ToolCall(tool_name=call.name, arguments=dict(call.args or {}))

    text = "".join(getattr(part, "text", None) or "" for part in parts).strip()
    if not text:
        raise ReasoningError("The provider returned neither a tool call nor a textual conclusion")

    return Finish(output=text)
