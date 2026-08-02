from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class StepReport(BaseModel):

    """

    Facade schema for one flattened step of a run trace.

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


class RunReport(BaseModel):

    """

    Facade schema for the concluded outcome of a run.

    """

    run_id: str
    goal: str
    status: Literal["completed", "exhausted", "failed"]
    output: str | None = None
    total_steps: int
    steps: list[StepReport] = Field(default_factory=list)
    started_at: datetime
    finished_at: datetime
