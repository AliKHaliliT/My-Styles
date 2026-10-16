# Invariants

What must stay true about this product, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. The rulebook's section on the invariants ledger defines the columns and the five rungs; the docs audit holds that every holder is in the tree and prints every claim held by review alone on every run, and whether a claim is true stays with review.

| Claim | Held by | Rung |
| --- | --- | --- |
| A marker that defers work, or a model's leftover, in living prose is named on every run. | `scripts/audit_inquiry.py` "VOCABULARY" | advised |
| Every evidence pin in a claim names a commit in this history. | `scripts/audit_inquiry.py` "check_pins" | impossible |
| Evidence that moved past its pin or its last verification is named on every run. | `scripts/audit_inquiry.py` "evidence paths moved past" | advised |
| Every manifest names a style the stale-pin scan has paths for. | `scripts/audit_inquiry.py` "check_manifest_style" | impossible |
| Two claims quoting one figure at one pin quote one value. | `scripts/audit_inquiry.py` "check_figures" | impossible |
| Every claim still standing is linked from a question, and every question links a claim or says it has none. | `scripts/audit_inquiry.py` "check_questions" | impossible |
| A pass added from the seed rule's arrival names its seeds in its Boundary, fixed, indexed and found never rising, each seed a key Found names, or says none. | `scripts/audit_inquiry.py` "check_review_seeds" | impossible |
| A pass added from the extension rule's arrival that extends another names the date it extends from, before the day the extended pass ran. | `scripts/audit_inquiry.py` "check_review_extension" | impossible |
| A pass added from the nearest-review rule's arrival names in its Boundary the review that already covers its slice, by key, or says none found. | `scripts/audit_inquiry.py` "check_review_nearest" | impossible |
| A pass added from the screening rule's arrival links a screening log that exists or says none, and the rows the linked log passed at the abstract stage are the funnel's screened count. | `scripts/audit_inquiry.py` "check_review_screening" | impossible |
| A screening log added from the rule's arrival opens with the header, names a reason for every exclusion, and leaves a record unsure at the abstract stage alone. | `scripts/audit_inquiry.py` "check_screening_logs" | impossible |
| An arrow's suite never checks a claim, and the audit never reaches into an arrow. | review | review |
| Read evidence a pass took from less than the whole work is named on every run while a Supported claim rests on it. | `scripts/audit_inquiry.py` "advise_shallow_reads" | advised |
| A Supported claim resting on a work below the declared evidence floor is named on every run. | `scripts/audit_inquiry.py` "advise_standing" | advised |
| A Supported claim resting on a work whose entry says retracted is named on every run, floor or none. | `scripts/audit_inquiry.py` "retracted since it was entered" | advised |
| A pass added from the retraction rule's arrival answers for retraction on its Checks line. | `scripts/audit_inquiry.py` "check_review_retraction" | impossible |
| A preprint unchecked for a published version for a season is named on every run. | `scripts/audit_inquiry.py` "advise_unchecked_preprints" | advised |
| An upstream entry carries no address, URL, email or absolute path. | `scripts/audit_inquiry.py` "check_upstream_entry" | impossible |
