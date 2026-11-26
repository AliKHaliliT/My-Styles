# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| A word spelled in the other variety in living prose is named on every run where codespell is installed. | `scripts/audit_docs.py` "en-GB_to_en-US" | advised |
| No tracked text file carries an invisible character, a generated file apart. | `scripts/audit_docs.py` "check_invisible" | impossible |
| No comment in the tree defers work with a marker. | `pyproject.toml` "FIX" | impossible |
| The domain and the services never import the web framework, the database layer, or the outer layers. | `pyproject.toml` "The core is framework-free" | impossible |
| A duplicate username is refused before the provider is touched. | `tests/app/services/test_user_service.py` "test_a_duplicate_username_is_refused_before_the_provider_is_touched" | listed cases |
| A malformed request is refused in the standard error shape. | `tests/test_main.py` "test_a_malformed_request_is_refused_in_the_standard_error_shape" | listed cases |
| A value a request validator refuses is answered as unprocessable, with the validator's own reason. | `tests/app/core/exception_handlers/test_validation_exception_handler.py` "test_a_value_a_validator_refuses_is_answered_as_unprocessable_with_its_reason" | listed cases |
| A constraint a model declares stands on its table and never inside a column, where a generated migration would pass over it. | `tests/db/test_base.py` "test_no_column_holds_a_constraint_a_generated_migration_would_pass_over" | listed cases |
| Every timestamp the API sends carries its offset. | `tests/app/api/v1/schemas/common/test_mixins.py` "test_a_stamp_the_database_wrote_crosses_the_wire_with_its_offset" | listed cases |
| A revision generated from the models applies as generated and names only the types the database stores. | `tests/db/migrations/test_env.py` "test_a_revision_generated_from_the_models_applies_and_names_only_what_the_database_stores" | listed cases |
| A schema whose fields are reordered keeps the bases, methods, validators and configuration its class statement gives it. | `tests/app/utils/test_reorder_fields.py` "test_the_validators_it_inherits_and_declares_still_refuse" | listed cases |
| The core never learns which provider implementation it drives. | review | review |
| No suite replaces a collaborator by patching a module's internals. | `scripts/audit_docs.py` "module mocking is banned" | impossible |
| An engine laid out as the engines README says is collected by the suite run, and its suites and ports pass the lint as the app's do. | `tests/test_engines.py` "test_the_suite_run_collects_an_engines_suites" | listed cases |
| An upstream entry carries no address, URL, email or absolute path. | `scripts/audit_docs.py` "check_upstream_entry" | impossible |
| A token is accepted only under the configured algorithm, so one signed with the right secret under another algorithm is refused. | `tests/app/core/security/test_local_auth.py` "test_a_token_signed_under_another_algorithm_is_refused" | listed cases |
| A token signed with another secret, or not signed at all, is refused. | `tests/app/core/security/test_local_auth.py` "test_an_unsigned_token_is_refused_whatever_its_claims_say" | listed cases |
| A token without its expiry or its subject is refused. | `tests/app/core/security/test_local_auth.py` "test_a_token_without_an_expiry_is_refused" | listed cases |
| The token algorithm is one of the HMAC family, since one shared secret both signs and verifies. | `app/core/config/settings.py` "enforce_hmac_algorithm" | impossible |
| The shared secret is at least as long as the configured algorithm's hash output. | `app/core/config/settings.py` "enforce_secret_length_for_algorithm" | impossible |
| An edition below the snapshot holds no path the workshop withholds, and its silent version names nothing of the style. | `scripts/cut_edition.py` "prove_silent" | listed cases |
| A file stripped for an edition differs from its source in comments and docstrings alone. | `scripts/cut_edition.py` "prove_strips" | listed cases |
