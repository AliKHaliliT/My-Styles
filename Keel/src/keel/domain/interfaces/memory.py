from typing import Protocol, runtime_checkable

from keel.domain.schemas.steps import StepRecord


@runtime_checkable
class IMemory(Protocol):

    """
    
    Interface defining the persistence surface for run transcripts.
    
    """

    async def record(self, run_id: str, entry: StepRecord) -> None: ...
    async def recall(self, run_id: str) -> list[StepRecord]: ...
    async def forget(self, run_id: str) -> None: ...
