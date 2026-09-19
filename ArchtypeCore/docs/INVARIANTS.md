# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| The domain and the services never import the web framework, the database layer, or the outer layers. | `pyproject.toml` "The core is framework-free" | impossible |
| Dependencies point one way, from the api through the services to the domain, never back. | `pyproject.toml` "The Dependency Rule points one way" | impossible |
| A duplicate username is refused before the provider is touched. | `tests/app/services/test_user_service.py` "test_a_duplicate_username_is_refused_before_the_provider_is_touched" | listed cases |
| A request id never outlives its request. | `tests/app/core/middlewares/observability/test_request_id_middleware.py` "test_the_id_does_not_outlive_the_request" | listed cases |
| A malformed request is refused in the standard error shape. | `tests/test_main.py` "test_a_malformed_request_is_refused_in_the_standard_error_shape" | listed cases |
| The core never learns which provider implementation it drives. | review | review |
