from typing import Protocol, runtime_checkable

from keel.domain.schemas.actions import Action
from keel.domain.schemas.runs import RunState
from keel.domain.schemas.tools import ToolSpec


@runtime_checkable
class IReasoner(Protocol):

    """

    Interface defining the decision-making capability of the engine.

    """

    async def decide(self, state: RunState, tools: list[ToolSpec]) -> Action: ...
