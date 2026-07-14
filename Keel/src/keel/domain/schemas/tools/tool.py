from typing import Any

from pydantic import BaseModel, Field


class ToolSpec(BaseModel):

    """

    Domain schema describing a tool's callable contract.

    """

    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):

    """

    Domain schema representing the outcome of a tool execution.

    """

    content: str
    is_error: bool = False
