from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class RunRequest(BaseModel):

    """
    
    API schema describing a requested run.
    
    """

    goal: str
    max_steps: int | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "goal": "calculate (2 + 3) * 4",
                "max_steps": 8
            }
        }
    )


class StepReport(BaseModel):

    """
    
    API schema for one flattened step of a run trace.
    
    """

    index: int
    action_type: Literal["tool_call", "finish"]
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    rationale: str | None = None
    result: str | None = None
    is_error: bool = False
    started_at: datetime
    finished_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "index": 0,
                "action_type": "tool_call",
                "tool_name": "calculator",
                "arguments": {"expression": "(2 + 3) * 4"},
                "rationale": "The goal asks for an arithmetic evaluation",
                "result": "20",
                "is_error": False,
                "started_at": "2026-07-14T12:00:00Z",
                "finished_at": "2026-07-14T12:00:01Z"
            }
        }
    )


class RunReport(BaseModel):

    """
    
    API schema for the concluded outcome of a run.
    
    """

    run_id: str
    goal: str
    status: Literal["completed", "exhausted", "failed"]
    output: str | None = None
    total_steps: int
    steps: list[StepReport] = Field(default_factory=list)
    started_at: datetime
    finished_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "run_id": "8f14e45fceea167a5a36dedd4bea2543",
                "goal": "calculate (2 + 3) * 4",
                "status": "completed",
                "output": "20",
                "total_steps": 2,
                "steps": [],
                "started_at": "2026-07-14T12:00:00Z",
                "finished_at": "2026-07-14T12:00:02Z"
            }
        }
    )
