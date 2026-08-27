# 0031. Hold living prose to the version story

Status: Accepted
Date: 2026-08-27

## Context

Record 0030 unified the version story to the one number CI executes, and the
sweep that landed it covered the config fields and stopped there. Two living
sentences kept the old floor: the AGENTS.md install line and the README's
getting-started line both still said Node 20.19+ after `engines` said 24. The
sweep's boundary, config fields only, was never named, and the sibling Python
trees carried the same rot in their own install lines.

A stale floor claim in a living document is exactly the rot the docs audit
exists to catch, a sentence true at writing that reality moved past through a
path that never touches the file. The audit had no rule for it.

## Decision

The docs audit gates every floor claim in living prose against the runtime the
tree declares, reading the floor from `engines.node` in `package.json` and
matching `Node N+` or `Node.js N+` in the living documents. A mismatch is a
problem, not advice, because both sides of the comparison are single declared
numbers.

Only a claim carrying the trailing plus is a floor claim. A bare version
mention could be talking about anything, and a check may never imply more than
it decides, so bare mentions stay review's. Decision records are exempt as
history.

The rule was proven before it was adopted. A planted stale claim failed the
audit in this tree and in each sibling, and the unplanted trees pass, so the
check demonstrably fires and demonstrably rests.

## Consequences

The next runtime bump cannot ship a stale install line, since the audit fails
until prose follows the fields, and the bump sweep no longer relies on a
remembered list. Keel and ArchtypeCore carry the Python form of the check in
their shared audit script.

The check decides number agreement and nothing more. Whether a sentence ought
to make a floor claim at all, and whether prose describes the runtime honestly
in every other way, stays with review.
