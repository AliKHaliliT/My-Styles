from keel.facade.schemas import RunReport, RunRequest
from keel.facade.translators import (domain_to_facade_run_report,
                                     facade_to_domain_run_request)
from keel.services.execution import AgentRunner


class Engine:

    """

    The public facade wrapping an assembled agent runner.


    Usage
    -----
    Consumers obtain an Engine from the EngineBuilder and interact with the
    facade's schemas only; the facade translates across the boundary in both
    directions and never leaks domain objects.
    ```python
    import asyncio

    from keel import EngineBuilder

    engine = EngineBuilder().build()
    report = asyncio.run(engine.run("calculate (2 + 3) * 4"))
    print(report.status, report.output)
    ```

    """

    def __init__(self, runner: AgentRunner) -> None:

        """

        Constructor for the Engine class.


        Parameters
        ----------
        runner : AgentRunner
            The assembled orchestration service.


        Returns
        -------
        None.


        Raises
        ------
        TypeError
            If `runner` is not an AgentRunner.

        """

        if not isinstance(runner, AgentRunner):
            raise TypeError(f"runner must be an AgentRunner. Received: {runner} with type {type(runner)}")


        self._runner = runner


    async def run(self, goal: str, max_steps: int | None = None) -> RunReport:

        """

        Executes a bounded run toward the given goal.


        Parameters
        ----------
        goal : str
            The natural-language goal for the run.

        max_steps : int | None, optional
            A per-run override of the configured step budget.


        Returns
        -------
        RunReport
            The concluded outcome, including the flattened step trace.


        Raises
        ------
        ValueError
            If `goal` is not a non-empty string, or `max_steps` is not a positive integer or None.

        """

        if not isinstance(goal, str) or not goal.strip():
            raise ValueError(f"goal must be a non-empty string. Received: {goal} with type {type(goal)}")
        if max_steps is not None and (not isinstance(max_steps, int) or max_steps < 1):
            raise ValueError(f"max_steps must be a positive integer or None. Received: {max_steps} with type {type(max_steps)}")


        request = RunRequest(goal=goal, max_steps=max_steps)
        domain_spec = facade_to_domain_run_request(request)
        domain_result = await self._runner.run(domain_spec)

        return domain_to_facade_run_report(domain_result)
