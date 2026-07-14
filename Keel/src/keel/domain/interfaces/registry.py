from typing import Protocol, runtime_checkable

from keel.domain.interfaces.tool import ITool
from keel.domain.schemas.tools import ToolSpec


@runtime_checkable
class IToolRegistry(Protocol):

    """
    
    Interface defining the lookup surface for registered tools.
    
    """

    def register(self, tool: ITool) -> None: ...
    def get(self, name: str) -> ITool: ...
    def specs(self) -> list[ToolSpec]: ...
