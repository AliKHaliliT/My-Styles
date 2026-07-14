from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EngineEvent(BaseModel):

    """
    
    Domain schema for a structured observability event emitted by the engine.
    
    """

    type: str
    run_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
