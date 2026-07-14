from importlib.metadata import entry_points

from keel.core.logging import get_logger
from keel.domain.interfaces import ITool

PLUGIN_GROUP = "keel.tools"

logger = get_logger("core.plugins")


def load_entry_point_tools(group: str = PLUGIN_GROUP) -> list[ITool]:

    """

    Discovers third-party tools published under an entry-point group.


    Usage
    -----
    A plugin is any installed distribution exposing an ITool implementation
    (a class or a zero-argument factory) under the group. Discovery is fault
    isolated: a plugin that fails to load, fails to construct, or does not
    satisfy the ITool contract is logged and skipped, never fatal; one broken
    third-party package must not take the engine down with it.
    ```python
    from keel.core.plugins import load_entry_point_tools

    tools = load_entry_point_tools()
    ```


    Parameters
    ----------
    group : str, optional
        The entry-point group to scan.


    Returns
    -------
    list[ITool]
        The successfully constructed tool implementations.


    Raises
    ------
    ValueError
        If `group` is not a non-empty string.

    """

    if not isinstance(group, str) or not group.strip():
        raise ValueError(f"group must be a non-empty string. Received: {group} with type {type(group)}")


    tools: list[ITool] = []

    for entry_point in entry_points(group=group):
        try:
            loaded = entry_point.load()
            candidate = loaded() if callable(loaded) and not isinstance(loaded, ITool) else loaded
        except Exception:
            logger.exception(f"Skipping plugin '{entry_point.name}': failed to load or construct")
            continue

        if not isinstance(candidate, ITool):
            logger.warning(f"Skipping plugin '{entry_point.name}': object does not implement ITool")
            continue

        tools.append(candidate)

    return tools
