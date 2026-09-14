# Project State

## Now

- Nothing in flight.

## Next

- Carry own-field defaults through `reorder_fields`, which reads them from the class and so drops them, and give the moved fields a fixed order where none is interleaved, which today follows set iteration; both with a test (2026-09-14)

## Deferred

- Reshape the check functions of `scripts/audit_docs.py` and the sync in `scripts/peer_sync.py` to fit the function-shape limits and drop the script exemption from the lint configuration (2026-09-14)

## Blocked

- Nothing blocked.
