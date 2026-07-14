from typing import Protocol, runtime_checkable

from keel.domain.schemas.events import EngineEvent


@runtime_checkable
class IEventSink(Protocol):

    """

    Interface defining the observability surface for engine events.

    """

    async def emit(self, event: EngineEvent) -> None: ...
