from keel.domain.schemas.actions import ToolCall
from keel.domain.schemas.runs import RunResult
from keel.domain.schemas.steps import StepRecord
from keel.facade.schemas import RunReport, StepReport


def domain_to_facade_step_report(record: StepRecord) -> StepReport:

    """

    Convert a domain StepRecord to a facade StepReport.

    """

    action = record.action
    tool_name = action.tool_name if isinstance(action, ToolCall) else None
    arguments = action.arguments if isinstance(action, ToolCall) else None

    return StepReport(
        index=record.index,
        action_type=action.kind,
        tool_name=tool_name,
        arguments=arguments,
        rationale=action.rationale,
        result=record.result.content if record.result is not None else None,
        is_error=record.result.is_error if record.result is not None else False,
        started_at=record.started_at,
        finished_at=record.finished_at,
    )


def domain_to_facade_run_report(result: RunResult) -> RunReport:

    """

    Convert a domain RunResult to a facade RunReport.

    """

    return RunReport(
        run_id=result.run_id,
        goal=result.goal,
        status=result.status,
        output=result.output,
        total_steps=len(result.steps),
        steps=[domain_to_facade_step_report(step) for step in result.steps],
        started_at=result.started_at,
        finished_at=result.finished_at,
    )
