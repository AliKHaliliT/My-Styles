from datetime import datetime

from pydantic import BaseModel, Field

from keel.domain.schemas.actions import Action
from keel.domain.schemas.tools import ToolResult


class StepRecord(BaseModel):

    """
    
    Domain schema recording a single iteration of the engine loop.
    
    """

    index: int
    action: Action = Field(discriminator="kind")
    result: ToolResult | None = None
    started_at: datetime
    finished_at: datetime
