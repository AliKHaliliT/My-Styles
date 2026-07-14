import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from keel.core.config import EngineConfig
from keel.core.logging import get_logger
from keel.domain.exceptions import (ReasoningError, StepLimitExceededError,
                                    ToolExecutionError, ToolNotFoundError)
from keel.domain.interfaces import (IEventSink, IMemory, IReasoner,
                                    IToolRegistry)
from keel.domain.schemas.actions import Finish, ToolCall
from keel.domain.schemas.events import EngineEvent
from keel.domain.schemas.runs import RunResult, RunSpec, RunState
from keel.domain.schemas.steps import StepRecord
from keel.domain.schemas.tools import ToolResult

logger = get_logger("services.execution")


class AgentRunner:

    """
    
    A service orchestrating the bounded reason -> act -> record loop.
    
    
    Usage
    -----
    This class is the single owner of the engine loop. It relies on abstract
    ports for every capability: an IReasoner for decisions, an IToolRegistry
    for lookups, an IMemory for transcripts, and an IEventSink for
    observability. Tool failures are captured as data and fed back to the
    reasoner (unless halting is configured), step budgets bound every run,
    and a broken event sink is logged without ever taking the run down.
    ```python
    from keel.services.execution import AgentRunner
    
    runner = AgentRunner(reasoner, registry, memory, events, config)
    result = await runner.run(RunSpec(goal="calculate (2 + 3) * 4"))
    print(result.status, result.output)
    ```
    
    """

    def __init__(
        self,
        reasoner: IReasoner,
        registry: IToolRegistry,
        memory: IMemory,
        events: IEventSink,
        config: EngineConfig,
    ) -> None:

        """
        
        Constructor for the AgentRunner class.
        
        
        Parameters
        ----------
        reasoner : IReasoner
            The decision-making interface.
        
        registry : IToolRegistry
            The tool lookup interface.
        
        memory : IMemory
            The transcript persistence interface.
        
        events : IEventSink
            The observability interface.
        
        config : EngineConfig
            The immutable runtime configuration.
        
        
        Returns
        -------
        None.
        
        """

        if not isinstance(reasoner, IReasoner):
            raise TypeError(f"reasoner must implement IReasoner. Received: {reasoner} with type {type(reasoner)}")
        if not isinstance(registry, IToolRegistry):
            raise TypeError(f"registry must implement IToolRegistry. Received: {registry} with type {type(registry)}")
        if not isinstance(memory, IMemory):
            raise TypeError(f"memory must implement IMemory. Received: {memory} with type {type(memory)}")
        if not isinstance(events, IEventSink):
            raise TypeError(f"events must implement IEventSink. Received: {events} with type {type(events)}")
        if not isinstance(config, EngineConfig):
            raise TypeError(f"config must be an EngineConfig. Received: {config} with type {type(config)}")


        self.reasoner = reasoner
        self.registry = registry
        self.memory = memory
        self.events = events
        self.config = config


    async def run(self, spec: RunSpec) -> RunResult:

        """
        
        Executes a bounded run for the given specification.
        
        
        Parameters
        ----------
        spec : RunSpec
            The specification describing the requested run.
        
        
        Returns
        -------
        RunResult
            The concluded outcome, including the full step trace.
        
        
        Raises
        ------
        StepLimitExceededError
            If the step budget is consumed while raise_on_exhaustion is configured.
        
        ToolExecutionError
            If a tool fails while halt_on_tool_error is configured.
        
        """

        if not isinstance(spec, RunSpec):
            raise TypeError(f"spec must be a RunSpec. Received: {spec} with type {type(spec)}")
        if spec.max_steps is not None and spec.max_steps < 1:
            raise ValueError(f"spec.max_steps must be a positive integer or None. Received: {spec.max_steps}")


        run_id = uuid4().hex
        max_steps = spec.max_steps if spec.max_steps is not None else self.config.max_steps
        state = RunState(run_id=run_id, goal=spec.goal, max_steps=max_steps)
        started_at = datetime.now(UTC)

        await self._emit("run.started", run_id, {"goal": spec.goal, "max_steps": max_steps})

        while state.steps_taken < state.max_steps:
            step_started_at = datetime.now(UTC)
            index = state.steps_taken

            try:
                action = await self.reasoner.decide(state, self.registry.specs())
                if not isinstance(action, (ToolCall, Finish)):
                    raise ReasoningError(f"The reasoner returned an invalid action. Received: {action} with type {type(action)}")
            except ReasoningError as error:
                await self._emit("run.failed", run_id, {"reason": str(error)})
                return RunResult(
                    run_id=run_id,
                    goal=spec.goal,
                    status="failed",
                    output=str(error),
                    steps=state.transcript,
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                )

            if isinstance(action, Finish):
                step = StepRecord(index=index, action=action, result=None, started_at=step_started_at, finished_at=datetime.now(UTC))
                state.transcript.append(step)
                await self.memory.record(run_id, step)
                await self._emit("run.completed", run_id, {"output": action.output, "steps_taken": state.steps_taken})
                return RunResult(
                    run_id=run_id,
                    goal=spec.goal,
                    status="completed",
                    output=action.output,
                    steps=state.transcript,
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                )

            await self._emit("step.started", run_id, {"index": index, "tool_name": action.tool_name})

            result = await self._execute_tool(action)

            step = StepRecord(index=index, action=action, result=result, started_at=step_started_at, finished_at=datetime.now(UTC))
            state.transcript.append(step)
            await self.memory.record(run_id, step)
            await self._emit("step.finished", run_id, {"index": index, "tool_name": action.tool_name, "is_error": result.is_error})

        await self._emit("run.exhausted", run_id, {"steps_taken": state.steps_taken, "max_steps": max_steps})

        if self.config.raise_on_exhaustion:
            raise StepLimitExceededError(f"Run '{run_id}' consumed its step budget of {max_steps}")

        return RunResult(
            run_id=run_id,
            goal=spec.goal,
            status="exhausted",
            output=None,
            steps=state.transcript,
            started_at=started_at,
            finished_at=datetime.now(UTC),
        )


    async def _execute_tool(self, action: ToolCall) -> ToolResult:

        """
        
        Executes a tool call under the configured timeout and error policy.
        
        
        Parameters
        ----------
        action : ToolCall
            The decided tool invocation.
        
        
        Returns
        -------
        ToolResult
            The execution outcome; failures become error results unless halting is configured.
        
        
        Raises
        ------
        ToolExecutionError
            If the tool fails while halt_on_tool_error is configured.
        
        """

        try:
            tool = self.registry.get(action.tool_name)
        except ToolNotFoundError as error:
            if self.config.halt_on_tool_error:
                raise
            return ToolResult(content=str(error), is_error=True)

        try:
            if self.config.step_timeout_seconds is not None:
                content = await asyncio.wait_for(tool.execute(action.arguments), timeout=self.config.step_timeout_seconds)
            else:
                content = await tool.execute(action.arguments)
        except TimeoutError as error:
            message = f"Tool '{action.tool_name}' timed out after {self.config.step_timeout_seconds} seconds"
            if self.config.halt_on_tool_error:
                raise ToolExecutionError(message) from error
            return ToolResult(content=message, is_error=True)
        except ToolExecutionError as error:
            if self.config.halt_on_tool_error:
                raise
            return ToolResult(content=str(error), is_error=True)
        except Exception as error:
            message = f"Tool '{action.tool_name}' raised an unexpected error: {error}"
            if self.config.halt_on_tool_error:
                raise ToolExecutionError(message) from error
            return ToolResult(content=message, is_error=True)

        if not isinstance(content, str):
            message = f"Tool '{action.tool_name}' returned a non-string result. Received: {content} with type {type(content)}"
            if self.config.halt_on_tool_error:
                raise ToolExecutionError(message)
            return ToolResult(content=message, is_error=True)

        return ToolResult(content=content)


    async def _emit(self, event_type: str, run_id: str, payload: dict[str, Any]) -> None:

        """
        
        Emits an engine event, isolating sink failures from the run.
        
        
        Parameters
        ----------
        event_type : str
            The dotted event type identifier.
        
        run_id : str
            The identifier of the run the event belongs to.
        
        payload : dict[str, Any]
            The structured event payload.
        
        
        Returns
        -------
        None.
        
        """

        event = EngineEvent(type=event_type, run_id=run_id, payload=payload, created_at=datetime.now(UTC))

        try:
            await self.events.emit(event)
        except Exception:
            logger.exception(f"Event sink failed while emitting '{event_type}' for run '{run_id}'")
