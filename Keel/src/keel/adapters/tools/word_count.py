from typing import Any

from keel.domain.exceptions import ToolExecutionError


class WordCountTool:

    """

    A tool counting the whitespace-delimited words in a text.


    Usage
    -----
    ```python
    from keel.adapters.tools import WordCountTool

    tool = WordCountTool()
    result = await tool.execute({"text": "the quick brown fox"})
    print(result)
    ```

    """

    name: str = "word_count"
    description: str = "Counts the whitespace-delimited words in the given text and returns the count."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text whose words should be counted",
            }
        },
        "required": ["text"],
    }


    async def execute(self, arguments: dict[str, Any]) -> str:

        """

        Counts the words in the text argument.


        Parameters
        ----------
        arguments : dict[str, Any]
            The tool arguments; requires a 'text' string.


        Returns
        -------
        str
            The word count rendered as a string.


        Raises
        ------
        TypeError
            If `arguments` is not a dictionary.

        ToolExecutionError
            If the text argument is missing or not a string.

        """

        if not isinstance(arguments, dict):
            raise TypeError(f"arguments must be a dictionary. Received: {arguments} with type {type(arguments)}")


        text = arguments.get("text")
        if not isinstance(text, str):
            raise ToolExecutionError(f"'text' must be a string. Received: {text}")

        return str(len(text.split()))
