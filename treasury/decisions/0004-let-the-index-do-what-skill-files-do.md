# 0004. Let the index do what skill files do

Status: Accepted
Date: 2026-08-18

## Context

The owner's notes held two related items for review: a published guide of
eleven principles for token-efficient work with coding agents, and the open
question of whether the styles should carry skill files, meaning packaged
instruction files that an agent loads only when a matching task triggers
them. Both were analyzed against the family's existing law rather than on
their own terms.

The guide's principles split by who they instruct. One half addresses the
person operating an agent: choosing model tiers, starting fresh sessions per
topic, undoing instead of stacking corrective prompts, delegating
output-heavy work. The other half addresses the shape of a repository, and
mapping it against the family showed convergence under older names:
iterating rules in the agent guide is the owned rulebook with the upstream
report, shifting verification left is the gate carried from the first line
written, bounding agent loops is the gate's own bounded loop, and specific
context is the index contract with bounded documents and one home per fact.
The guide's stated problem, context bloat, is what the document budgets and
fission already solve, justified by rot and reader attention rather than by
token cost.

Skill files were tested against the one condition that earns them: a
procedure that recurs, is needed only on trigger, and currently either
bloats an always-loaded document or gets re-explained despite being written
down. Measured concretely, the three agent guides run 79 to 83 lines, every
section but one is needed on every task, and the one trigger-shaped
resident, the upstream report, is thirteen lines. There is nothing to move.

## Options considered

- Adopt skill files now. Rejected three ways: they add a third home for
  procedural knowledge to a system whose agent guide and indexed documents
  already form the two loading tiers skills exist to provide, inviting the
  drift the single-source and intent-split items exist to prevent; their
  packaging is still vendor-flavored while the family's bet is the
  vendor-neutral agent guide; and with no recurring pain on record they are
  speculative scaffolding, which the Waste item names.
- Add token cost as a rationale to the existing document rules. Rejected: a
  rule justified by an extra reason invites wrong extensions, and rot and
  reader attention are the durable justifications.
- Adopt the operator-side principles as style law. Rejected: a style is law
  for a repository, not a manual for the person driving the tool.

## Decision

Nothing is adopted. The two-tier loading the family already runs, an
always-loaded agent guide that earns every line and indexed documents
fetched when a task touches them, is the ruling mechanism, and the index
does what skill files would do. The rejection is standing but context-bound,
and three conditions reopen it: a section of the agent guide or rulebook
that only some tasks need grows past what every session should pay to load;
a documented procedure demonstrably gets re-explained across sessions, which
would mean the index is failing as discovery; or skill packaging
standardizes across vendors to the point where adopting it no longer bets on
one tool.

## Consequences

The guide's repository-side half stays enforced under the family's existing
names, and its operator-side half stays out of the law. One observation is
kept because it strengthens the treasury's premise. Token efficiency is not
a new discipline but the optimization vocabulary applied to a new scarce
resource, delegation as offloading, verification shifted left as the cheap
filter before the expensive judge, session hygiene as working-set
management. The names change per field; the operations do not.
