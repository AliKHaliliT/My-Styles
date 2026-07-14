from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ITool(Protocol):

    """
    
    Interface defining an executable capability the engine can invoke.
    
    """

    name: str
    description: str
    parameters: dict[str, Any]

    async def execute(self, arguments: dict[str, Any]) -> str: ...
