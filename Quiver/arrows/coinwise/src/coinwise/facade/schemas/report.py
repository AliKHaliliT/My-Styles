from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class StrategyReport:

    """

    Facade schema for what one strategy did to the accumulated stream.

    """

    rounded_total: Decimal
    exact_total: Decimal
    drift: Decimal
    tie_count: int


@dataclass(frozen=True)
class ExperimentReport:

    """

    Facade schema for both strategies' results over one deterministic grid.

    """

    count: int
    half_up: StrategyReport
    half_even: StrategyReport
