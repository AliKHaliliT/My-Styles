# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| Every evidence pin in a claim names a commit in this history. | `scripts/audit_inquiry.py` "check_pins" | impossible |
| Evidence that moved past its pin or its last verification is named on every run. | `scripts/audit_inquiry.py` "evidence paths moved past" | advised |
| Every manifest names a style the stale-pin scan has paths for. | `scripts/audit_inquiry.py` "check_manifest_style" | impossible |
| Two claims quoting one figure at one pin quote one value. | `scripts/audit_inquiry.py` "check_figures" | impossible |
| Every claim still standing is linked from a question, and every question links a claim or says it has none. | `scripts/audit_inquiry.py` "check_questions" | impossible |
| An arrow's suite never checks a claim, and the audit never reaches into an arrow. | review | review |
| Read evidence a pass took from less than the whole work is named on every run while a Supported claim rests on it. | `scripts/audit_inquiry.py` "advise_shallow_reads" | advised |
| A Supported claim resting on a work below the declared evidence floor is named on every run. | `scripts/audit_inquiry.py` "advise_standing" | advised |
| A preprint unchecked for a published version for a season is named on every run. | `scripts/audit_inquiry.py` "advise_unchecked_preprints" | advised |
| An upstream entry carries no address, URL, email or absolute path. | `scripts/audit_inquiry.py` "check_upstream_entry" | impossible |
