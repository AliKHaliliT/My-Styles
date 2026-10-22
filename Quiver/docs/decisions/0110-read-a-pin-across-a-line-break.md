# 0110. Read a pin across a line break

Status: Accepted
Date: 2026-10-22

## Context

A claim's run evidence names its pin as `arrows/<name> at <commit-
hash>`, and the audit's matcher required one space on each side of the
word at. A record wraps at seventy-two columns, so the space before the
hash may be a line break, and a pin wrapped there was read by nothing.
The pin check did not test the commit, the manifest check did not count
the claim and the stale-pin advisory never named it, while the audit
also refused nothing, so the record passed as if it carried no run
evidence at all. A project built from this template met the case in a
claim inventory that counted one run-evidence record more than the
matcher.

## Options considered

- Refuse the wrapped spelling as malformed. Refused, because the
  spelling is the rule's own form with a line break the wrapping rule
  put there, and a record admits no edit to unwrap it.
- Leave the matcher and ask records to keep the pin on one line.
  Refused, because a rule that depends on where a line happens to break
  is met by accident.

## Decision

The pin matcher reads any whitespace between the arrow, the word at and
the hash, so a pin wrapped at the line break is the same pin, held by
the commit check, counted by the manifest check and watched by the
stale-pin advisory. The selftest plants a claim whose pin wraps and
expects the commit finding under it, and the claims rule says the audit
reads a pin across the break.

## Consequences

A run-evidence record is held wherever its pin falls on the line, and a
wrapped record that escaped the checks is read from now on.
