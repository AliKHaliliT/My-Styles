import json
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from keel.adapters.reasoners.gemini.domain_to_provider import (
    domain_to_provider_contents, domain_to_provider_tools)
from keel.adapters.reasoners.gemini.provider_to_domain import \
    provider_to_domain_action
from keel.domain.exceptions import ReasoningError
from keel.domain.schemas.actions import Finish, ToolCall
from keel.domain.schemas.runs import RunState
from keel.domain.schemas.steps import StepRecord
from keel.domain.schemas.tools import ToolResult, ToolSpec

# The translators speak plain dictionaries on the way out and duck-typed attributes on the
# way in, so this suite runs without the SDK installed, which keeps CI offline. The fixture
# case replays a response recorded from one real API call, when that recording exists.

STAMP = datetime(2026, 1, 1, tzinfo=UTC)
FIXTURE = Path(__file__).resolve().parents[6] / "fixtures" / "gemini-decide.json"


def to_namespace(value: Any) -> Any:
    """Rebuild the SDK's attribute surface from recorded JSON; call args stay a mapping."""
    if isinstance(value, dict):
        return SimpleNamespace(**{
            k: v if k == "args" else to_namespace(v) for k, v in value.items()
        })
    if isinstance(value, list):
        return [to_namespace(v) for v in value]
    return value


def make_state_with_one_tool_step() -> RunState:
    state = RunState(run_id="r1", goal="count words in the quick brown fox", max_steps=8)
    state.transcript.append(
        StepRecord(
            index=0,
            action=ToolCall(tool_name="word_count", arguments={"text": "the quick brown fox"}),
            result=ToolResult(content="4"),
            started_at=STAMP,
            finished_at=STAMP,
        )
    )
    return state


def test_tools_become_one_declaration_block_with_json_schemas() -> None:
    specs = [ToolSpec(name="word_count", description="Counts words", parameters={"type": "object"})]
    tools = domain_to_provider_tools(specs)
    assert tools[0]["function_declarations"][0]["name"] == "word_count"
    assert tools[0]["function_declarations"][0]["parameters_json_schema"] == {"type": "object"}


def test_a_spec_without_parameters_gets_an_empty_object_schema() -> None:
    specs = [ToolSpec(name="clock", description="Tells the time")]
    schema = domain_to_provider_tools(specs)[0]["function_declarations"][0]["parameters_json_schema"]
    assert schema == {"type": "object", "properties": {}}


def test_the_transcript_becomes_alternating_call_and_response_turns() -> None:
    contents = domain_to_provider_contents(make_state_with_one_tool_step())
    assert contents[0] == {"role": "user", "parts": [{"text": "count words in the quick brown fox"}]}
    assert contents[1]["role"] == "model"
    assert contents[1]["parts"][0]["function_call"]["name"] == "word_count"
    assert contents[2]["role"] == "user"
    assert contents[2]["parts"][0]["function_response"]["response"]["content"] == "4"


def test_a_function_call_part_becomes_a_tool_call() -> None:
    response = to_namespace({
        "prompt_feedback": None,
        "candidates": [{"content": {"parts": [
            {"function_call": {"name": "word_count", "args": {"text": "hi"}}, "text": None},
        ]}}],
    })
    action = provider_to_domain_action(response)
    assert isinstance(action, ToolCall)
    assert action.tool_name == "word_count"
    assert action.arguments == {"text": "hi"}


def test_text_parts_become_a_finish() -> None:
    response = to_namespace({
        "prompt_feedback": None,
        "candidates": [{"content": {"parts": [
            {"function_call": None, "text": "Four words."},
        ]}}],
    })
    action = provider_to_domain_action(response)
    assert isinstance(action, Finish)
    assert action.output == "Four words."


def test_a_blocked_prompt_raises_a_reasoning_error() -> None:
    response = to_namespace({"prompt_feedback": {"block_reason": "SAFETY"}, "candidates": []})
    with pytest.raises(ReasoningError):
        provider_to_domain_action(response)


def test_an_empty_response_raises_a_reasoning_error() -> None:
    response = to_namespace({"prompt_feedback": None, "candidates": []})
    with pytest.raises(ReasoningError):
        provider_to_domain_action(response)


@pytest.mark.skipif(not FIXTURE.exists(), reason="the recorded live response is not present yet")
def test_the_recorded_live_response_still_parses() -> None:
    recorded = json.loads(FIXTURE.read_text(encoding="utf-8"))
    action = provider_to_domain_action(to_namespace(recorded))
    assert isinstance(action, (ToolCall, Finish))
