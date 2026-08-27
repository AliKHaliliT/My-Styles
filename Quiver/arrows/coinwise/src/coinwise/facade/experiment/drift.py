from dataclasses import dataclass
from decimal import Decimal

from coinwise.domain.rounding import round_half_even, round_half_up
from coinwise.services.accumulation import DriftResult, accumulate


@dataclass(frozen=True)
class ExperimentReport:

    """

    Both strategies' results over one deterministic grid of amounts.


    Usage
    -----
    One call runs the whole experiment; the count fixes the grid, the
    grid fixes the ties, and the report carries one DriftResult per
    strategy over the identical amounts.
    ```python
    from coinwise.facade.experiment import run_drift_experiment

    report = run_drift_experiment(1000)
    print((report.half_up.drift, report.half_even.drift))
    ```

    """

    count: int
    half_up: DriftResult
    half_even: DriftResult


def grid_amounts(count: int) -> list[Decimal]:

    """

    Builds the deterministic three-decimal amount grid.

    The grid is every multiple of a tenth of a cent from one count
    upward, so its tie density is fixed by construction at one in ten
    and every run is exactly reproducible with no seed.


    Parameters
    ----------
    count : int
        How many amounts to generate.


    Returns
    -------
    list[Decimal]
        The values i divided by one thousand for i from 1 to `count`,
        each carrying exactly three decimal places.


    Raises
    ------
    ValueError
        If `count` is smaller than one.

    """

    if count < 1:
        raise ValueError(f"count must be at least 1. Received: {count} with type {type(count)}")


    return [Decimal(i) / 1000 for i in range(1, count + 1)]


def run_drift_experiment(count: int) -> ExperimentReport:

    """

    Accumulates one grid under both strategies and reports the drifts.


    Parameters
    ----------
    count : int
        How many grid amounts to accumulate.


    Returns
    -------
    ExperimentReport
        Both strategies' totals, drifts, and the shared tie count.


    Raises
    ------
    ValueError
        If `count` is smaller than one.

    """

    amounts = grid_amounts(count)
    return ExperimentReport(
        count=count,
        half_up=accumulate(amounts, round_half_up),
        half_even=accumulate(amounts, round_half_even),
    )
