from keel.domain.exceptions import DuplicateToolError, ToolNotFoundError
from keel.domain.interfaces import ITool
from keel.domain.schemas.tools import ToolSpec


class ToolRegistry:

    """

    A duplicate-safe registry mapping tool names to implementations.


    Usage
    -----
    The registry is the single lookup surface the engine loop trusts. Names
    are unique; registering the same name twice raises immediately at wiring
    time instead of silently shadowing a tool at run time.
    ```python
    from keel.adapters.registry import ToolRegistry

    registry = ToolRegistry()
    registry.register(YourTool())

    tool = registry.get("your_tool")
    specs = registry.specs()
    ```

    """

    def __init__(self) -> None:

        """

        Constructor for the ToolRegistry class.


        Parameters
        ----------
        None.


        Returns
        -------
        None.


        Raises
        ------
        None.

        """

        self._tools: dict[str, ITool] = {}


    def register(self, tool: ITool) -> None:

        """

        Registers a tool under its declared name.


        Parameters
        ----------
        tool : ITool
            The tool implementation to register.


        Returns
        -------
        None.


        Raises
        ------
        TypeError
            If `tool` does not implement ITool.

        DuplicateToolError
            If a tool with the same name is already registered.

        """

        if not isinstance(tool, ITool):
            raise TypeError(f"tool must implement ITool. Received: {tool} with type {type(tool)}")


        if tool.name in self._tools:
            raise DuplicateToolError(f"Tool with name '{tool.name}' is already registered")

        self._tools[tool.name] = tool


    def get(self, name: str) -> ITool:

        """

        Fetches a registered tool by name.


        Parameters
        ----------
        name : str
            The name of the tool to retrieve.


        Returns
        -------
        ITool
            The registered tool implementation.


        Raises
        ------
        ValueError
            If `name` is not a non-empty string.

        ToolNotFoundError
            If no tool is registered under the given name.

        """

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"name must be a non-empty string. Received: {name} with type {type(name)}")


        if name not in self._tools:
            raise ToolNotFoundError(f"Tool with name '{name}' is not registered")

        return self._tools[name]


    def specs(self) -> list[ToolSpec]:

        """

        Returns the callable contracts of every registered tool.


        Parameters
        ----------
        None.


        Returns
        -------
        list[ToolSpec]
            The specifications, ordered by registration.


        Raises
        ------
        None.

        """

        return [
            ToolSpec(name=tool.name, description=tool.description, parameters=tool.parameters)
            for tool in self._tools.values()
        ]
