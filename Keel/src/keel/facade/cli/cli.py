import argparse
import asyncio

from keel.facade.engine import EngineBuilder

_EXIT_CODES = {
    "completed": 0,
    "failed": 1,
    "exhausted": 2,
}


def build_parser() -> argparse.ArgumentParser:

    """

    Builds the argument parser for the console entry point.


    Parameters
    ----------
    None.


    Returns
    -------
    argparse.ArgumentParser
        The configured parser.


    Raises
    ------
    None.

    """

    parser = argparse.ArgumentParser(
        prog="keel",
        description="Run the offline demo engine toward a natural-language goal.",
    )
    parser.add_argument("goal", help='The goal to run, e.g. "calculate (2 + 3) * 4"')
    parser.add_argument("--max-steps", type=int, default=None, help="Override the configured step budget for this run")
    parser.add_argument("--show-trace", action="store_true", help="Print the step trace after the output")

    return parser


def main(argv: list[str] | None = None) -> int:

    """

    Entry point for the console script and module execution.


    Parameters
    ----------
    argv : list[str] | None, optional
        The argument vector; None defers to sys.argv.


    Returns
    -------
    int
        0 on completion, 1 on failure, 2 on step-budget exhaustion.


    Raises
    ------
    None.

    """

    arguments = build_parser().parse_args(argv)

    engine = EngineBuilder().build()
    report = asyncio.run(engine.run(arguments.goal, max_steps=arguments.max_steps))

    print(report.output if report.output is not None else f"(no output; run {report.status} after {report.total_steps} steps)")

    if arguments.show_trace:
        for step in report.steps:
            if step.action_type == "tool_call":
                print(f"  [{step.index}] tool_call {step.tool_name}({step.arguments}) -> {'ERROR: ' if step.is_error else ''}{step.result}")
            else:
                print(f"  [{step.index}] finish -> {step.result if step.result is not None else report.output}")

    return _EXIT_CODES[report.status]
