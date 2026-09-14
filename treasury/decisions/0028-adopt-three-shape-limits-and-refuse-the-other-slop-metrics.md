# 0028. Adopt three shape limits and refuse the other slop metrics

Status: Accepted
Date: 2026-09-14

## Context

The owner brought a study of agent-written code that measured it against
established repositories on two borrowed metrics, verbosity, the share of
duplicated or flagged lines, and erosion, the share of a codebase's mass in
functions whose cyclomatic complexity is above ten, and found agent code about
twice as bad on both. Its benchmark ran many rounds with the context wiped
between them and saw even the strongest models solve nothing under strict
scoring, because decisions accumulate across sessions and no session sees the
whole. The family had no check that counted forks. The question was which of
the classic static metrics to fold in, as a check that decides itself rather
than as another sentence asking for taste.

## Evidence

The complexity rule at ten, run over the family on 2026-09-14 before any
change:

| Seat | Product code above ten | Scripts above ten |
| --- | --- | --- |
| Keel | 1 | 7 |
| ArchtypeCore | 4 | 8 |
| Quiver, host and arrow | 0 | 15 |
| Helm, by ESLint | 0 | 0 |

Nesting deeper than five occurred in four script functions and no product
function; more than fifty statements in two product functions, both in the
ArchtypeCore field reorderer, and four script functions. Every script finding
was a check function whose branches are the rules it checks, the largest the
Quiver selftest at fifty-five paths. The Python dead-code tool printed sixteen
findings on Keel and over a hundred on ArchtypeCore with the sampled ones
false, and the TypeScript one flagged twenty exports and types on Helm, every
one a slice's public surface exposed on purpose. Helm passed all three limits
with no finding.

## Options considered

- Adopting the study's own ratios, verbosity and erosion over a whole tree.
  Refused. A ratio is gamed through its denominator, and a tree-wide number
  names no function to fix, where the per-function limit behind erosion does.
- Cognitive complexity, which weights nesting more heavily. Deferred, because
  the Python linter does not compute it and the nesting limit covers the shape
  it would add.
- Dead-code detection, clone counting, blended maintainability scores, and
  churn hotspots. Refused for the template on the evidence above and for the
  reasons the seat records give.
- Recording the ruling only here. Refused, because the ruling changes every
  seat's bytes, so each seat carries its own record under 0001.

## Decision

Every seat gates three function-shape limits with its linter, ten paths
through a function, five nested blocks, and fifty statements, exempting its
audit scripts in configuration as debt its STATE.md names. The seats record
the ruling as Keel 0053, ArchtypeCore 0050, and Helm 0054, identical bodies,
and the arrow inherits Keel's. This record carries the family's disposition of
the study, one metric adopted in per-function form and the rest refused or
deferred, with the measurements that decided it.

## Consequences

The next study of code quality starts from these measurements instead of
repeating them. A future seat adopts the three limits with its own linter on
arrival. The refused metrics stay refused until a project, not a template,
shows one of them deciding a real question.
