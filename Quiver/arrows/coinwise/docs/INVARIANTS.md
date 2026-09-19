# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| Dependencies point one way, from the facade through the services to the domain, never back. | `pyproject.toml` "The Dependency Rule points one way" | impossible |
| The two strategies agree on every amount that is not a tie. | `tests/src/coinwise/domain/rounding/test_strategies.py` "test_property_the_strategies_agree_on_every_amount_that_is_not_a_tie" | generated cases |
| No strategy moves an amount by more than half a cent. | `tests/src/coinwise/domain/rounding/test_strategies.py` "test_property_no_strategy_moves_an_amount_by_more_than_half_a_cent" | generated cases |
| Half even lands every tie on an even cent. | `tests/src/coinwise/domain/rounding/test_strategies.py` "test_property_half_even_lands_every_tie_on_an_even_cent" | generated cases |
| On the experiment's grid, half up drifts half a cent per tie while half even cancels. | `tests/src/coinwise/facade/experiment/test_drift.py` "test_half_up_drifts_half_a_cent_per_tie_while_half_even_cancels" | listed cases |
| The grid's tie density is one in ten by construction. | `tests/src/coinwise/facade/experiment/test_drift.py` "test_the_grid_tie_density_is_one_in_ten_by_construction" | listed cases |
