# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| Every evidence pin in a claim names a commit in this history. | `scripts/audit_inquiry.py` "check_pins" | impossible |
| Evidence that moved past its pin or its last verification is named on every run. | `scripts/audit_inquiry.py` "evidence paths moved past" | advised |
| Two claims quoting one figure at one pin quote one value. | `scripts/audit_inquiry.py` "check_figures" | impossible |
| An arrow's suite never checks a claim, and the audit never reaches into an arrow. | review | review |
