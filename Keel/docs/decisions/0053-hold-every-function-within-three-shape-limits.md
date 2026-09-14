# 0053. Hold every function within three shape limits

Status: Accepted
Date: 2026-09-14

## Context

A study of code written by agents measured it against established
repositories and found it about twice as eroded, meaning that its mass sat in
large branching functions, and about twice as verbose. The mechanism showed in
a benchmark that runs many rounds with the context wiped between them. Each
feature adds a fork to a function that already exists rather than a function
that does not, and no round sees the maze grow. The family's checks counted
docstrings, imports, and layer crossings and never counted forks, so a worker
could add the twentieth branch to a function and every light stayed green. The
delivery gate names cognitive load and granularity, but as judgment items, and
a judgment item binds only a reader who already agrees with it.

## Evidence

The complexity rule at ten, run over the family on 2026-09-14 before any
change:

| Seat | Product code above ten | Scripts above ten |
| --- | --- | --- |
| Keel | 1 | 7 |
| ArchtypeCore | 4 | 8 |
| Quiver, host and arrow | 0 | 15 |
| Helm, by ESLint | 0 | 0 |

The product findings were the Keel tool executor at twelve and, in
ArchtypeCore, the field reorderer at fifty-one with its inner decorator at
thirty-nine, and the example generator at twenty-three with its type
placeholder at sixteen. Nesting deeper than five occurred in four script
functions and no product function. More than fifty statements occurred in the
two reorderer functions and in four script functions. Every script finding was
a check function whose branches are the rules it checks, the largest the
Quiver selftest at fifty-five paths. Dead-code tools were measured too. The
Python one printed sixteen findings on Keel and over a hundred on ArchtypeCore
with the sampled ones false, interface methods, request parameters, adapters
wired at runtime, and the TypeScript one flagged twenty exports and types on
Helm, every one a slice's public surface.

## Options considered

- An advisory warning rather than a gate. Refused, because a path count is
  decided by the tool entirely, so the two-tier rule places it in the gating
  tier, and an advisory over the audit scripts would print the same standing
  findings on every run, which trains dismissal.
- A suppression comment as the answer to a finding. Refused, because the guide
  forbids silencing a warning that way, and a gate answered by a comment has
  stopped gating.
- Cognitive complexity, which weights nesting. Deferred; it measures the
  gate's cognitive-load item more closely, but the Python linter does not
  compute it and the nesting limit covers the shape it would add.
- Dead-code detection. Refused for the template, on the evidence above; worth
  revisiting in a project, where the public surface has consumers.
- Clone counting, blended maintainability scores, and churn hotspots.
  Refused. Clones surface in review on trees this size, a blended score hides
  which thing is wrong, and a hotspot is a report over a history a template
  does not have.

## Decision

A function stays within three limits, ten paths through it, five nested
blocks, and fifty statements, and the linter gates all three with the rest of
the lint. Ten is McCabe's original threshold and the one the study used to
define erosion; five and fifty are the linter's own defaults, stated rather
than inherited. The audit scripts are exempt in the linter's configuration
with the reason beside the exemption, because a check function carries one
branch per rule and splitting it would scatter the rules, and the exemption is
a debt each STATE.md names. A finding is answered by splitting the function,
moving a repeated block into one helper, or turning a branch chain into a
table. A type guard is carried intact into the piece that needs it and never
removed to lower a count. A function that genuinely needs more is a conflict
under the pause rule, put to the owner, never a suppression.

## Consequences

Five product functions were reshaped before the rule landed, so it arrived on
a green tree, and the Keel change put the tool executor's halt policy in one
place instead of five. The gate's cognitive-load and granularity items keep
their judgment half and gain a decidable floor. A worker adding a branch to a
full function is stopped at lint rather than at review. The nesting rule is
still in the Python linter's preview set, so the configuration names it
explicitly and admits nothing else from preview. The audit scripts stay
outside the limits until each is reshaped, which their STATE entries track,
the largest first.
