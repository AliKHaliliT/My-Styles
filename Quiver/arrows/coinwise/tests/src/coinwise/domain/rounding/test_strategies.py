from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from coinwise.domain.rounding import is_tie, round_half_even, round_half_up

# The gate must reproduce from a pinned tree, so every property runs
# derandomized with no example database; free-roaming randomness stays a
# local exploration tool. A green property test claims no counterexample
# in its generated cases, not a proof (decision 0035).
AMOUNTS = st.decimals(
    min_value=Decimal("0.000"), max_value=Decimal("1000000.000"), places=3, allow_nan=False, allow_infinity=False
)
TIES = st.integers(min_value=0, max_value=100_000_000).map(lambda cents: Decimal(cents) / 100 + Decimal("0.005"))


def test_half_up_breaks_a_tie_away_from_zero() -> None:
    assert round_half_up(Decimal("0.005")) == Decimal("0.01")
    assert round_half_up(Decimal("0.015")) == Decimal("0.02")


def test_half_even_breaks_a_tie_toward_the_even_cent() -> None:
    assert round_half_even(Decimal("0.005")) == Decimal("0.00")
    assert round_half_even(Decimal("0.015")) == Decimal("0.02")


def test_the_strategies_agree_on_every_amount_that_is_not_a_tie() -> None:
    for thousandths in range(10):
        amount = Decimal("0.12") + Decimal(thousandths) / 1000
        if not is_tie(amount):
            assert round_half_up(amount) == round_half_even(amount)


def test_a_tie_splits_the_strategies_only_when_rounding_up_lands_odd() -> None:
    assert round_half_up(Decimal("0.125")) != round_half_even(Decimal("0.125"))
    assert round_half_up(Decimal("0.115")) == round_half_even(Decimal("0.115"))


def test_is_tie_fires_only_on_the_exact_half_cent() -> None:
    assert is_tie(Decimal("3.145"))
    assert not is_tie(Decimal("3.144"))
    assert not is_tie(Decimal("3.14"))


@given(amount=AMOUNTS)
@settings(derandomize=True, database=None)
def test_property_the_strategies_agree_on_every_amount_that_is_not_a_tie(amount: Decimal) -> None:
    if not is_tie(amount):
        assert round_half_up(amount) == round_half_even(amount)


@given(amount=TIES)
@settings(derandomize=True, database=None)
def test_property_a_tie_splits_the_strategies_exactly_when_rounding_up_lands_odd(amount: Decimal) -> None:
    split = round_half_up(amount) != round_half_even(amount)
    assert split == (round_half_up(amount) * 100 % 2 == 1)


@given(amount=AMOUNTS)
@settings(derandomize=True, database=None)
def test_property_no_strategy_moves_an_amount_by_more_than_half_a_cent(amount: Decimal) -> None:
    assert abs(round_half_up(amount) - amount) <= Decimal("0.005")
    assert abs(round_half_even(amount) - amount) <= Decimal("0.005")


@given(amount=AMOUNTS)
@settings(derandomize=True, database=None)
def test_property_rounding_an_already_rounded_amount_changes_nothing(amount: Decimal) -> None:
    assert round_half_up(round_half_up(amount)) == round_half_up(amount)
    assert round_half_even(round_half_even(amount)) == round_half_even(amount)


@given(amount=TIES)
@settings(derandomize=True, database=None)
def test_property_every_tie_costs_half_up_exactly_half_a_cent(amount: Decimal) -> None:
    assert is_tie(amount)
    assert round_half_up(amount) - amount == Decimal("0.005")


@given(amount=TIES)
@settings(derandomize=True, database=None)
def test_property_half_even_lands_every_tie_on_an_even_cent(amount: Decimal) -> None:
    assert round_half_even(amount) * 100 % 2 == 0
