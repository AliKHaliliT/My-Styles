from decimal import Decimal

from coinwise.domain.rounding import is_tie, round_half_even, round_half_up


def test_half_up_breaks_a_tie_away_from_zero() -> None:
    assert round_half_up(Decimal("0.005")) == Decimal("0.01")
    assert round_half_up(Decimal("0.015")) == Decimal("0.02")


def test_half_even_breaks_a_tie_toward_the_even_cent() -> None:
    assert round_half_even(Decimal("0.005")) == Decimal("0.00")
    assert round_half_even(Decimal("0.015")) == Decimal("0.02")


def test_the_strategies_agree_everywhere_except_at_a_tie() -> None:
    for thousandths in range(10):
        amount = Decimal("0.12") + Decimal(thousandths) / 1000
        if is_tie(amount):
            assert round_half_up(amount) != round_half_even(amount)
        else:
            assert round_half_up(amount) == round_half_even(amount)


def test_is_tie_fires_only_on_the_exact_half_cent() -> None:
    assert is_tie(Decimal("3.145"))
    assert not is_tie(Decimal("3.144"))
    assert not is_tie(Decimal("3.14"))
