# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| The domain and the services never import the facade, an adapter, or the vendor SDK. | `pyproject.toml` "The core stays inside the ports" | impossible |
| Dependencies point one way, from the facade through the services to the domain, never back. | `pyproject.toml` "The Dependency Rule points one way" | impossible |
| A step report carries its record across the facade boundary without loss or invention. | `tests/src/keel/facade/translators/test_domain_to_facade.py` "test_property_a_step_report_carries_its_record_without_loss" | generated cases |
| A run report counts and orders every step of its run. | `tests/src/keel/facade/translators/test_domain_to_facade.py` "test_property_a_run_report_counts_and_orders_every_step" | generated cases |
| The step budget bounds a reasoner that never finishes. | `tests/src/keel/services/execution/test_agent_runner.py` "test_the_step_budget_bounds_a_reasoner_that_never_finishes" | listed cases |
| A broken event sink never takes the run down. | `tests/src/keel/services/execution/test_agent_runner.py` "test_a_broken_event_sink_never_takes_the_run_down" | listed cases |
| A broken plugin found at build time is logged and skipped, never fatal. | review | review |
