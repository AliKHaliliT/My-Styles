# 0052. Prove the docs audit against planted defects

Status: Accepted
Date: 2026-09-15

## Context

The host audit has carried a selftest since it was written, one plant per
rule, because a check that never fires and a check that cannot fire look
identical. The docs audits in the three Python seats and in Helm never had
one. Their rules were proven by the adoption rehearsal, which shows the green
path in a shaped child, and this week by a differential run in a scratchpad
that compared each reshaped audit with its previous version over planted
trees. That run proved the reshaping and then died with the session. The
family's own principle says plants prove every rule, and a proof outside the
tree is a proof the tree does not carry. Reshaping every audit under the shape
limits made the gap concrete, since every split rested on a harness nobody
could rerun tomorrow.

## Options considered

- Keep the differential harness in the tree. Refused. It proves that two
  versions agree, so it needs an old version to run against, and a rule needs
  a proof of itself, not of its last diff.
- Rely on the rehearsal. Refused. A child whose gate passes proves that the
  audit runs clean where it should, never that it fires where it should.
- Prove only the rules that changed this week. Refused. A partial proof
  reads as a proof, and the next reader cannot tell which rules it covers.

## Decision

The docs audit gains a `--selftest`, modelled on the host's. The unplanted
tree is checked first and the command stops with the audit's own findings if
it is not clean. Then one plant per rule builds what it needs and removes
what it built, a tracked plant enters the index by intent-to-add and leaves
it again, and a borrowed living file comes back byte for byte. A rule that
only history can plant, or that the tooling cannot be made to miss, is named
as skipped in the output rather than counted as proven. The selftest runs in
CI before the audit, in each seat's own workflow, and in the rehearsal, which
requires every rule to fire in the shaped child and the child's tree to be
unchanged afterwards. Helm's audit gains the same in its own language.

## Consequences

Every rule of the docs audit has a proof the tree carries and CI runs, in the
template and in a project built from it, where the preconditions differ. The
scratchpad harness retires. The two import-graph rules and the queue-age rule
stand as named gaps rather than silent ones. A change to the audit is
proven the way the host's has always been, by running the proof first.
