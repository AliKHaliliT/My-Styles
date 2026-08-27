"""The drift experiment the inquiry's claims cite, runnable in one call."""

from dataclasses import dataclass
from decimal import Decimal

from coinwise.domain.rounding import round_half_even, round_half_up
from coinwise.services.accumulation import DriftResult, accumulate


@dataclass(frozen=True)
class ExperimentReport:
    """Both strategies' results over one deterministic grid of amounts.

    Usage
    -----
    >>> from coinwise.facade.experiment import run_drift_experiment
    >>> report = run_drift_experiment(1000)
    >>> (report.half_up.drift, report.half_even.drift)
    (Decimal('0.500'), Decimal('0.000'))

    Attributes
    ----------
    count : int
        How many grid amounts were accumulated.
    half_up : DriftResult
        The accumulation under round-half-up.
    half_even : DriftResult
        The accumulation under round-half-even.
    """

    count: int
    half_up: DriftResult
    half_even: DriftResult


def grid_amounts(count: int) -> list[Decimal]:
    """Build the deterministic three-decimal amount grid.

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
        amounts: the values i divided by one thousand for i from 1 to
        count, each carrying exactly three decimal places.

    Raises
    ------
    ValueError
        If count is smaller than one.
    """
    if count < 1:
        raise ValueError("count must be at least 1")
    return [Decimal(i) / 1000 for i in range(1, count + 1)]


def run_drift_experiment(count: int) -> ExperimentReport:
    """Accumulate one grid under both strategies and report the drifts.

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
        If count is smaller than one.
    """
    amounts = grid_amounts(count)
    return ExperimentReport(
        count=count,
        half_up=accumulate(amounts, round_half_up),
        half_even=accumulate(amounts, round_half_even),
    )
