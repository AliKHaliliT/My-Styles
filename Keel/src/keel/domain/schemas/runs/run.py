from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from keel.domain.schemas.steps import StepRecord

RunStatus = Literal["completed", "exhausted", "failed"]


class RunSpec(BaseModel):

    """

    Domain schema describing a requested run.

    """

    goal: str
    max_steps: int | None = None


class RunState(BaseModel):

    """

    Domain schema for the evolving state the reasoner decides against.

    """

    run_id: str
    goal: str
    max_steps: int
    transcript: list[StepRecord] = Field(default_factory=list)

    @property
    def steps_taken(self) -> int:
        return len(self.transcript)

    @property
    def remaining_steps(self) -> int:
        return self.max_steps - len(self.transcript)


class RunResult(BaseModel):

    """

    Domain schema for the concluded outcome of a run.

    """

    run_id: str
    goal: str
    status: RunStatus
    output: str | None = None
    steps: list[StepRecord] = Field(default_factory=list)
    started_at: datetime
    finished_at: datetime
