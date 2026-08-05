from typing import Any

import pytest

from keel.adapters.events import CollectingEventSink
from keel.adapters.memory import InMemoryMemory
from keel.adapters.registry import ToolRegistry
from keel.core.config import EngineConfig
from keel.domain.exceptions import StepLimitExceededError, ToolExecutionError
from keel.domain.schemas.actions import Action, Finish, ToolCall
from keel.domain.schemas.events import EngineEvent
from keel.domain.schemas.runs import RunSpec, RunState
from keel.domain.schemas.tools import ToolSpec
from keel.services.execution import AgentRunner

# The registry, the transcript, and the event sink are the shipped adapters, because each is
# already deterministic and in-process. Only the two ports that reach outside in production,
# the reasoner and a tool, are stood in for here, and both are hand-written against their
# interface rather than patched into place.


class ScriptedReasoner:

    def __init__(self, *actions: Action) -> None:
        self.remaining = list(actions)
        self.offered_tools: list[list[str]] = []
        self.seen_transcript_lengths: list[int] = []

    async def decide(self, state: RunState, tools: list[ToolSpec]) -> Action:
        self.offered_tools.append([spec.name for spec in tools])
        self.seen_transcript_lengths.append(len(state.transcript))
        if not self.remaining:
            return Finish(output="the script ran out")
        return self.remaining.pop(0)


class ScriptedTool:

    def __init__(self, name: str = "echo", returns: str = "done", raises: Exception | None = None) -> None:
        self.name = name
        self.description = f"the {name} tool"
        self.parameters: dict[str, Any] = {}
        self.returns = returns
        self.raises = raises
        self.calls: list[dict[str, Any]] = []

    async def execute(self, arguments: dict[str, Any]) -> str:
        self.calls.append(arguments)
        if self.raises is not None:
            raise self.raises
        return self.returns


class BrokenEventSink:

    async def emit(self, event: EngineEvent) -> None:
        raise RuntimeError("the sink is down")


def build_runner(*actions: Action, tool: ScriptedTool | None = None, **config: Any) -> tuple[AgentRunner, ScriptedReasoner, InMemoryMemory, CollectingEventSink]:
    reasoner = ScriptedReasoner(*actions)
    registry = ToolRegistry()
    if tool is not None:
        registry.register(tool)
    memory = InMemoryMemory()
    events = CollectingEventSink()
    runner = AgentRunner(reasoner, registry, memory, events, EngineConfig(**config))
    return runner, reasoner, memory, events


def event_types(events: CollectingEventSink) -> list[str]:
    return [event.type for event in events.events]


async def test_a_finish_action_completes_the_run_and_records_one_step() -> None:
    runner, reasoner, memory, events = build_runner(Finish(output="42"))

    result = await runner.run(RunSpec(goal="answer the question"))

    assert result.status == "completed"
    assert result.output == "42"
    assert len(result.steps) == 1
    assert await memory.recall(result.run_id) == result.steps
    assert event_types(events) == ["run.started", "run.completed"]


async def test_a_tool_call_runs_before_the_next_decision_and_its_result_is_recorded() -> None:
    tool = ScriptedTool(returns="the tool spoke")
    runner, reasoner, memory, events = build_runner(
        ToolCall(tool_name="echo", arguments={"text": "hello"}),
        Finish(output="finished"),
        tool=tool,
    )

    result = await runner.run(RunSpec(goal="use the tool"))

    assert result.status == "completed"
    assert tool.calls == [{"text": "hello"}]
    assert len(result.steps) == 2

    tool_step = result.steps[0]
    assert tool_step.result is not None
    assert tool_step.result.content == "the tool spoke"
    assert tool_step.result.is_error is False

    # The reasoner saw the registry's specs, and saw the first step before deciding again.
    assert reasoner.offered_tools == [["echo"], ["echo"]]
    assert reasoner.seen_transcript_lengths == [0, 1]
    assert event_types(events) == ["run.started", "step.started", "step.finished", "run.completed"]


async def test_a_failing_tool_becomes_data_the_reasoner_can_read() -> None:
    tool = ScriptedTool(raises=ToolExecutionError("the tool broke"))
    runner, reasoner, memory, events = build_runner(
        ToolCall(tool_name="echo"),
        Finish(output="recovered"),
        tool=tool,
    )

    result = await runner.run(RunSpec(goal="survive a failure"))

    assert result.status == "completed"
    assert result.output == "recovered"

    failed_step = result.steps[0]
    assert failed_step.result is not None
    assert failed_step.result.is_error is True
    assert "the tool broke" in failed_step.result.content


async def test_a_failing_tool_halts_the_run_when_the_config_says_so() -> None:
    tool = ScriptedTool(raises=ToolExecutionError("the tool broke"))
    runner, reasoner, memory, events = build_runner(
        ToolCall(tool_name="echo"),
        tool=tool,
        halt_on_tool_error=True,
    )

    with pytest.raises(ToolExecutionError):
        await runner.run(RunSpec(goal="halt on a failure"))


async def test_an_unknown_tool_is_reported_without_ending_the_run() -> None:
    runner, reasoner, memory, events = build_runner(
        ToolCall(tool_name="missing"),
        Finish(output="carried on"),
    )

    result = await runner.run(RunSpec(goal="ask for a tool that is not there"))

    assert result.status == "completed"
    assert result.steps[0].result is not None
    assert result.steps[0].result.is_error is True


async def test_the_step_budget_bounds_a_reasoner_that_never_finishes() -> None:
    tool = ScriptedTool()
    runner, reasoner, memory, events = build_runner(
        *[ToolCall(tool_name="echo") for _ in range(5)],
        tool=tool,
    )

    result = await runner.run(RunSpec(goal="loop forever", max_steps=2))

    assert result.status == "exhausted"
    assert result.output is None
    assert len(result.steps) == 2
    assert tool.calls == [{}, {}]
    assert event_types(events)[-1] == "run.exhausted"


async def test_exhaustion_raises_when_the_config_says_so() -> None:
    tool = ScriptedTool()
    runner, reasoner, memory, events = build_runner(
        ToolCall(tool_name="echo"),
        tool=tool,
        raise_on_exhaustion=True,
    )

    with pytest.raises(StepLimitExceededError):
        await runner.run(RunSpec(goal="exhaust the budget", max_steps=1))


async def test_a_broken_event_sink_never_takes_the_run_down() -> None:
    runner = AgentRunner(
        ScriptedReasoner(Finish(output="unaffected")),
        ToolRegistry(),
        InMemoryMemory(),
        BrokenEventSink(),
        EngineConfig(),
    )

    result = await runner.run(RunSpec(goal="ignore a broken sink"))

    assert result.status == "completed"
    assert result.output == "unaffected"


async def test_a_non_positive_step_budget_is_refused() -> None:
    runner, reasoner, memory, events = build_runner(Finish(output="never reached"))

    with pytest.raises(ValueError):
        await runner.run(RunSpec(goal="ask for no steps", max_steps=0))


async def test_a_collaborator_that_does_not_satisfy_its_port_is_refused() -> None:
    with pytest.raises(TypeError):
        AgentRunner(object(), ToolRegistry(), InMemoryMemory(), CollectingEventSink(), EngineConfig())  # type: ignore[arg-type]  # the guard under test rejects this

    with pytest.raises(TypeError):
        AgentRunner(ScriptedReasoner(), ToolRegistry(), InMemoryMemory(), object(), EngineConfig())  # type: ignore[arg-type]  # the guard under test rejects this
