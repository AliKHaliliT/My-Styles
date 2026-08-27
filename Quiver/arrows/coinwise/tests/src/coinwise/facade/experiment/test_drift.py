from decimal import Decimal

import pytest

from coinwise.facade.experiment import grid_amounts, run_drift_experiment


def test_the_grid_is_deterministic_and_three_decimal() -> None:
    amounts = grid_amounts(3)
    assert amounts == [Decimal("0.001"), Decimal("0.002"), Decimal("0.003")]


def test_the_grid_refuses_an_empty_experiment() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        grid_amounts(0)


def test_the_grid_tie_density_is_one_in_ten_by_construction() -> None:
    report = run_drift_experiment(1000)
    assert report.half_up.tie_count == 100
    assert report.half_even.tie_count == 100


def test_half_up_drifts_half_a_cent_per_tie_while_half_even_cancels() -> None:
    report = run_drift_experiment(1000)
    assert report.half_up.drift == Decimal("0.500")
    assert report.half_even.drift == Decimal("0.000")
    assert report.half_up.exact_total == report.half_even.exact_total
