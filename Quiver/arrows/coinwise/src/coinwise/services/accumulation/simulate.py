"""Accumulate rounded amounts and measure the drift a strategy leaves behind."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from decimal import Decimal

from coinwise.domain.rounding import is_tie


@dataclass(frozen=True)
class DriftResult:
    """What one strategy did to one stream of amounts.

    Usage
    -----
    >>> from decimal import Decimal
    >>> from coinwise.domain.rounding import round_half_up
    >>> from coinwise.services.accumulation import accumulate
    >>> result = accumulate([Decimal("0.005"), Decimal("0.015")], round_half_up)
    >>> (result.drift, result.tie_count)
    (Decimal('0.010'), 2)

    Attributes
    ----------
    rounded_total : Decimal
        The sum of the amounts after each was rounded to cents.
    exact_total : Decimal
        The sum of the amounts with no rounding at all.
    drift : Decimal
        The rounded total minus the exact total, the error the
        strategy accumulated.
    tie_count : int
        How many amounts sat exactly halfway between two cents, the
        only inputs on which strategies can differ.
    """

    rounded_total: Decimal
    exact_total: Decimal
    drift: Decimal
    tie_count: int


def accumulate(
    amounts: Iterable[Decimal],
    strategy: Callable[[Decimal], Decimal],
) -> DriftResult:
    """Sum a stream of amounts twice, rounded per item and exactly.

    Parameters
    ----------
    amounts : Iterable[Decimal]
        The exact amounts to accumulate, in any order.
    strategy : Callable[[Decimal], Decimal]
        The rounding applied to each amount before the rounded sum.

    Returns
    -------
    DriftResult
        Both totals, their difference, and the tie count.

    Raises
    ------
    None.
    """
    rounded_total = Decimal("0")
    exact_total = Decimal("0")
    tie_count = 0
    for amount in amounts:
        rounded_total += strategy(amount)
        exact_total += amount
        if is_tie(amount):
            tie_count += 1
    return DriftResult(
        rounded_total=rounded_total,
        exact_total=exact_total,
        drift=rounded_total - exact_total,
        tie_count=tie_count,
    )
