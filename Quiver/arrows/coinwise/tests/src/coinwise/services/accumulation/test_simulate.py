from decimal import Decimal

from coinwise.domain.rounding import round_half_even, round_half_up
from coinwise.services.accumulation import accumulate

TWO_TIES = [Decimal("0.005"), Decimal("0.015")]


def test_half_up_drift_is_one_half_cent_per_tie() -> None:
    result = accumulate(TWO_TIES, round_half_up)
    assert result.rounded_total == Decimal("0.03")
    assert result.exact_total == Decimal("0.020")
    assert result.drift == Decimal("0.010")
    assert result.tie_count == 2


def test_half_even_ties_cancel_when_parities_balance() -> None:
    result = accumulate(TWO_TIES, round_half_even)
    assert result.rounded_total == Decimal("0.02")
    assert result.drift == Decimal("0.000")
    assert result.tie_count == 2


def test_an_empty_stream_accumulates_nothing() -> None:
    result = accumulate([], round_half_up)
    assert result.rounded_total == Decimal("0")
    assert result.exact_total == Decimal("0")
    assert result.drift == Decimal("0")
    assert result.tie_count == 0
