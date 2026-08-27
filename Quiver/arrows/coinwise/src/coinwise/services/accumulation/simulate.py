from collections.abc import Callable, Iterable
from dataclasses import dataclass
from decimal import Decimal

from coinwise.domain.rounding import is_tie


@dataclass(frozen=True)
class DriftResult:

    """

    What one strategy did to one stream of amounts.


    Usage
    -----
    The totals come from `accumulate`, which sums a stream twice, once
    rounding each amount with the strategy under test and once exactly.
    Drift is the rounded total minus the exact total, so a positive
    drift means the strategy overstated the ledger, and the tie count
    says how many amounts could have gone either way.
    ```python
    from decimal import Decimal

    from coinwise.domain.rounding import round_half_up
    from coinwise.services.accumulation import accumulate

    result = accumulate([Decimal("0.005"), Decimal("0.015")], round_half_up)
    print((result.drift, result.tie_count))
    ```

    """

    rounded_total: Decimal
    exact_total: Decimal
    drift: Decimal
    tie_count: int


def accumulate(
    amounts: Iterable[Decimal],
    strategy: Callable[[Decimal], Decimal],
) -> DriftResult:

    """

    Sums a stream of amounts twice, rounded per item and exactly.


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
