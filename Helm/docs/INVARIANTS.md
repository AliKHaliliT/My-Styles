# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| Imports point downward only, from app through pages, features, and entities to shared, never back up. | `eslint.config.js` "Imports point downward only" | impossible |
| A slice is entered through its index and never reached inside. | `eslint.config.js` "Enter a slice through its index.ts" | impossible |
| All HTTP goes through the shared request, and the environment is read through the shared config alone. | `eslint.config.js` "All HTTP goes through shared/api's request" | impossible |
| A payload that breaks the wire contract is refused before it reaches a component. | `tests/src/shared/api/client.test.ts` "refuses a payload that breaks the wire contract" | listed cases |
| A 401 on any query or mutation signs the session out. | `tests/src/app/providers.test.ts` "signs out when a query errors with 401" | listed cases |
| Nulls on the wire stay null in the domain instead of becoming invented values. | `tests/src/entities/vessel/translate.test.ts` "keeps nulls null instead of inventing values" | listed cases |
| The mock backend is wired only when the build is not for production. | review | review |
