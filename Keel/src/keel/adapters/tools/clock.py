from datetime import UTC, datetime
from typing import Any


class ClockTool:

    """

    A tool reporting the current UTC date and time.


    Usage
    -----
    This is the deliberately side-effecting demo tool: its output differs on
    every call, which is exactly the kind of dependency the engine keeps
    behind a tool boundary instead of letting it leak into domain logic.
    ```python
    from keel.adapters.tools import ClockTool

    tool = ClockTool()
    result = await tool.execute({})
    print(result)
    ```

    """

    name: str = "clock"
    description: str = "Returns the current UTC date and time in ISO 8601 format."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {},
    }


    async def execute(self, arguments: dict[str, Any]) -> str:

        """

        Returns the current UTC timestamp.


        Parameters
        ----------
        arguments : dict[str, Any]
            The tool arguments; none are required.


        Returns
        -------
        str
            The current UTC time in ISO 8601 format.


        Raises
        ------
        TypeError
            If `arguments` is not a dictionary.

        """

        if not isinstance(arguments, dict):
            raise TypeError(f"arguments must be a dictionary. Received: {arguments} with type {type(arguments)}")


        return datetime.now(UTC).isoformat()
