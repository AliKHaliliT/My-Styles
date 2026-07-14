from keel.adapters.events import LoggingEventSink
from keel.adapters.memory import InMemoryMemory
from keel.adapters.reasoners.rule_based import RuleBasedReasoner
from keel.adapters.registry import ToolRegistry
from keel.adapters.tools import CalculatorTool, ClockTool, WordCountTool
from keel.core.config import EngineConfig
from keel.core.logging import get_logger
from keel.core.plugins import load_entry_point_tools
from keel.domain.exceptions import DuplicateToolError
from keel.domain.interfaces import IEventSink, IMemory, IReasoner, ITool
from keel.facade.engine.engine import Engine
from keel.services.execution import AgentRunner

logger = get_logger("api.builder")


class EngineBuilder:

    """

    A guarded fluent builder assembling an Engine from its ports.


    Usage
    -----
    Every injected implementation is validated against its Protocol at wiring
    time, so a misconfigured engine fails at build, not mid-run. Anything not
    provided falls back to the offline defaults: the RuleBasedReasoner, the
    InMemoryMemory, the LoggingEventSink, the built-in demo tools, and a
    default EngineConfig.
    ```python
    from keel import EngineBuilder

    engine = (
        EngineBuilder()
        .with_config(EngineConfig(max_steps=4))
        .with_tool(YourTool())
        .build()
    )
    ```

    """

    def __init__(self) -> None:

        """

        Constructor for the EngineBuilder class.


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

        self._reasoner: IReasoner | None = None
        self._memory: IMemory | None = None
        self._events: IEventSink | None = None
        self._config: EngineConfig | None = None
        self._tools: list[ITool] = []
        self._include_default_tools: bool = True
        self._discover_plugins: bool = False


    def with_reasoner(self, reasoner: IReasoner) -> "EngineBuilder":

        """

        Injects the decision-making implementation.


        Parameters
        ----------
        reasoner : IReasoner
            The reasoner implementation to use.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `reasoner` does not implement IReasoner.

        """

        if not isinstance(reasoner, IReasoner):
            raise TypeError(f"reasoner must implement IReasoner. Received: {reasoner} with type {type(reasoner)}")


        self._reasoner = reasoner
        return self


    def with_memory(self, memory: IMemory) -> "EngineBuilder":

        """

        Injects the transcript persistence implementation.


        Parameters
        ----------
        memory : IMemory
            The memory implementation to use.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `memory` does not implement IMemory.

        """

        if not isinstance(memory, IMemory):
            raise TypeError(f"memory must implement IMemory. Received: {memory} with type {type(memory)}")


        self._memory = memory
        return self


    def with_event_sink(self, events: IEventSink) -> "EngineBuilder":

        """

        Injects the observability implementation.


        Parameters
        ----------
        events : IEventSink
            The event sink implementation to use.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `events` does not implement IEventSink.

        """

        if not isinstance(events, IEventSink):
            raise TypeError(f"events must implement IEventSink. Received: {events} with type {type(events)}")


        self._events = events
        return self


    def with_config(self, config: EngineConfig) -> "EngineBuilder":

        """

        Injects the runtime configuration.


        Parameters
        ----------
        config : EngineConfig
            The immutable configuration to use.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `config` is not an EngineConfig.

        """

        if not isinstance(config, EngineConfig):
            raise TypeError(f"config must be an EngineConfig. Received: {config} with type {type(config)}")


        self._config = config
        return self


    def with_tool(self, tool: ITool) -> "EngineBuilder":

        """

        Adds a tool to the engine's registry.


        Parameters
        ----------
        tool : ITool
            The tool implementation to register at build time.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `tool` does not implement ITool.

        """

        if not isinstance(tool, ITool):
            raise TypeError(f"tool must implement ITool. Received: {tool} with type {type(tool)}")


        self._tools.append(tool)
        return self


    def without_default_tools(self) -> "EngineBuilder":

        """

        Excludes the built-in demo tools from the registry.


        Parameters
        ----------
        None.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        None.

        """

        self._include_default_tools = False
        return self


    def with_discovered_tools(self) -> "EngineBuilder":

        """

        Opts in to entry-point tool discovery at build time.


        Parameters
        ----------
        None.


        Returns
        -------
        EngineBuilder
            The builder, for chaining.


        Raises
        ------
        None.

        """

        self._discover_plugins = True
        return self


    def build(self) -> Engine:

        """

        Assembles the Engine from the collected parts and defaults.


        Parameters
        ----------
        None.


        Returns
        -------
        Engine
            The ready-to-run engine facade.


        Raises
        ------
        None.

        """

        registry = ToolRegistry()

        if self._include_default_tools:
            registry.register(CalculatorTool())
            registry.register(WordCountTool())
            registry.register(ClockTool())

        for tool in self._tools:
            registry.register(tool)

        if self._discover_plugins:
            for tool in load_entry_point_tools():
                try:
                    registry.register(tool)
                except DuplicateToolError:
                    logger.warning(f"Skipping discovered tool '{tool.name}': the name is already registered")

        runner = AgentRunner(
            reasoner=self._reasoner if self._reasoner is not None else RuleBasedReasoner(),
            registry=registry,
            memory=self._memory if self._memory is not None else InMemoryMemory(),
            events=self._events if self._events is not None else LoggingEventSink(),
            config=self._config if self._config is not None else EngineConfig(),
        )

        return Engine(runner)
