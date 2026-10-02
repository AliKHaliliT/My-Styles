# 0069. Keep the ledger and refuse a confidence score

Status: Accepted
Date: 2026-10-02

## Context

A reader of this template meets a ledger of claims, conjectures, refuted
claims and open lines where a research agent of the current kind keeps a
compressed state inside one model's context and emits a confidence score,
and the question arrives why the template does not do the same. Two
preprints read on 2026-10-02 give the question a measured answer. One
reports that deep-search agents find a right answer among many samples far
more often than they select it, that verifying a candidate against a
question's conditions costs a fraction of finding it, and that a verifier
spent on the candidates buys more accuracy per call than more searching
[zeng2025]. The other builds that verification into the agent as an inner
loop keeping a state of six fields and an outer loop that accepts a
provisional answer above a confidence threshold, refines it from what was
verified, or discards the trajectory and restarts [lu2026].

## Evidence

The six fields of the state the agent keeps are verified findings with
their source identifiers, current candidates, unresolved constraints,
validity concerns, rejected candidates, and the next-step plan [lu2026].
Each has a home in this template already.

| Field of the agent's state | Where the template keeps it |
| --- | --- |
| Verified findings with source identifiers | Supported claims, quoting their evidence with a pin or a key |
| Current candidates | Conjectures |
| Unresolved constraints | The open lines of the decomposition |
| Validity concerns | The Threats section of every claim |
| Rejected candidates | Refuted claims, each with what would reopen it |
| Next-step plan | The Next and Blocked sections of the state file |

The ablation measures what such a state is worth. On BrowseComp the agent
scores 59.6 with neither the state nor the outer loop, 71.4 with the state
alone, and 82.5 with both, so the state adds 11.8 points and the outer loop
a further 11.1 [lu2026]. When the agent refreshes its state it preserves
the next-step plan 96.4 percent of the time, unresolved constraints 95.5,
rejected candidates 81.5 and verified findings 72.1, and two thirds of the
refreshes follow a revised search strategy [lu2026]. The confidence score
separates less well than the state. Of correct answers, 95.9 percent score
between 90 and 100, while 55.2 percent of wrong answers score below 60, so
the rest of the wrong answers score 60 or above, and when no round clears
the threshold the system returns the answer with the highest score
[lu2026]. The verification asymmetry is measured in tool calls. One model
spends about 75.3 calls finding a BrowseComp candidate and 18 verifying
it, and a verifier lifts its accuracy from 35.7 to 45.0 for about 100
extra calls where more searching lifts it to 40.8 for about 560; another
model finds a right answer among 16 samples 34 percent of the time and
selects it by majority vote about 12 percent of the time [zeng2025]. Both
works were read in their arXiv renderings on 2026-10-02, the method,
result and discussion sections whole and the appendices not.

## Options considered

- A confidence score on a claim or a pass, with a threshold that accepts
  without review. Refused. The score is a self-report that four wrong
  answers in nine clear at 60, the fallback returns the highest score when
  none clears, and the rule that a check never implies more than it
  decides forbids a number standing in for a verdict. The template's
  facets, depth, standing, funnel, pin and status, decide less and each
  decides what it says. Reopens if a score is calibrated on this
  inquiry's own records with its missed errors named and counted.
- Restarting by discarding a pass whose trajectory proved noisy. Refused.
  A dead end is evidence in an inquiry a person owns across sessions, the
  pass record that moved nothing and the refuted claim with its reopening
  condition are its form, and the agent's own state keeps rejected
  candidates in four refreshes of five for the same reason. Reopens if a
  landed pass is ever measured to mislead the next more than it informs it.
- A six-field state document beside the ledger. Refused, because every
  field already has a record a check reads, and a second copy rots.
- A verifier stage added to the pass. Refused, since the completeness
  review and the reading in full are that stage, and the funnel line now
  shows where a pass spent, on finding or on checking.

## Decision

The ledger stays the inquiry's state, held in records a check reads rather
than in a context a model rewrites, no claim or pass carries a confidence
score, and a pass that moved nothing lands as the record it is. The two
readings enter the bibliography as preprints with the day they were
checked for a published version, and this record holds the mapping and the
measurements, so the next reader who asks for a confidence score finds the
figures that refuse it.

## Consequences

The template has a measured case for its ledger from outside itself, 11.8
points for the state and 11.1 for the loop that reads it, and a measured
case against the scalar it refuses. The asymmetry result is the budget
rule for a pass, since the cheap half of research is checking what was
found, which the depth mark and the funnel line make visible and the
completeness review spends on.
