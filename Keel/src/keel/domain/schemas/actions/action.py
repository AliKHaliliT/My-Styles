from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCall(BaseModel):

    """

    Domain schema for a decision to invoke a tool.

    """

    kind: Literal["tool_call"] = "tool_call"
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    rationale: str | None = None


class Finish(BaseModel):

    """

    Domain schema for a decision to conclude the run.

    """

    kind: Literal["finish"] = "finish"
    output: str
    rationale: str | None = None


Action = ToolCall | Finish
