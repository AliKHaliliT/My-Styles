from datetime import datetime

from hypothesis import given, settings
from hypothesis import strategies as st

from keel.domain.schemas.actions import Finish, ToolCall
from keel.domain.schemas.runs import RunResult
from keel.domain.schemas.steps import StepRecord
from keel.domain.schemas.tools import ToolResult
from keel.facade.translators import (domain_to_facade_run_report,
                                     domain_to_facade_step_report)

# The gate must reproduce on every run, so every property runs derandomized
# with no example database; free-roaming randomness stays a local exploration
# tool. A green property test claims no counterexample in its generated
# cases, not a proof (decision 0035).
TEXT = st.text(max_size=20)
INSTANTS = st.datetimes(min_value=datetime(2026, 1, 1), max_value=datetime(2026, 12, 31))
ACTIONS = st.one_of(
    st.builds(
        ToolCall,
        tool_name=TEXT,
        arguments=st.dictionaries(TEXT, st.one_of(st.integers(), st.booleans(), TEXT), max_size=3),
        rationale=st.none() | TEXT,
    ),
    st.builds(Finish, output=TEXT, rationale=st.none() | TEXT),
)
STEPS = st.builds(
    StepRecord,
    index=st.integers(min_value=0, max_value=100),
    action=ACTIONS,
    result=st.none() | st.builds(ToolResult, content=TEXT, is_error=st.booleans()),
    started_at=INSTANTS,
    finished_at=INSTANTS,
)
RUNS = st.builds(
    RunResult,
    run_id=TEXT,
    goal=TEXT,
    status=st.sampled_from(["completed", "exhausted", "failed"]),
    output=st.none() | TEXT,
    steps=st.lists(STEPS, max_size=5),
    started_at=INSTANTS,
    finished_at=INSTANTS,
)


@given(record=STEPS)
@settings(derandomize=True, database=None)
def test_property_a_step_report_carries_its_record_without_loss(record: StepRecord) -> None:
    report = domain_to_facade_step_report(record)

    assert report.index == record.index
    assert report.action_type == record.action.kind
    assert report.rationale == record.action.rationale
    assert (report.started_at, report.finished_at) == (record.started_at, record.finished_at)
    if isinstance(record.action, ToolCall):
        assert report.tool_name == record.action.tool_name
        assert report.arguments == record.action.arguments
    else:
        assert report.tool_name is None
        assert report.arguments is None
    if record.result is None:
        assert report.result is None
        assert report.is_error is False
    else:
        assert report.result == record.result.content
        assert report.is_error == record.result.is_error


@given(result=RUNS)
@settings(derandomize=True, database=None)
def test_property_a_run_report_counts_and_orders_every_step(result: RunResult) -> None:
    report = domain_to_facade_run_report(result)

    assert report.total_steps == len(result.steps)
    assert [step.index for step in report.steps] == [step.index for step in result.steps]
    assert (report.run_id, report.goal, report.status, report.output) == (
        result.run_id,
        result.goal,
        result.status,
        result.output,
    )
