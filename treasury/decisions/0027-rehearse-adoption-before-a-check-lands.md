# 0027. Rehearse adoption before a check lands

Status: Accepted
Date: 2026-09-10

## Context

Four defects in one week were found by projects rather than by the family,
and three of them shared a cause: a check proven only in the template is
proven where its preconditions are absent. The template carries no inherited
folder, no upstream file, its own records from 0001, files written with bare
line feeds, and no commit older than the rule under test; a project built
from it has the opposite of every one of those. The plants that assumed the
template's tree, the byte comparisons that a Windows checkout silenced, and
the calendar comparison that judged a same-day record were each green here
and red in the first project that ran them. The owner asked whether these
were the kind of defect only operation can find, and the honest answer was
that a copy of the template shaped like a project would have found three of
the four in minutes.

## Decision

The family workflow rehearses adoption on every change. A script builds a
child from each seat in a temporary repository: the template copied whole,
its records moved into an inherited folder, its own decision record numbered
after them so none is 0001, an upstream file with an aligned line and one
entry, a long-named record committed before the audit arrives, a queued
entry, two commits with the audit arriving in the second, and a checkout with
Windows line endings. The child's docs audit must pass, the host seat's
selftest must report every rule firing, and the tree must be unchanged
afterwards. The script is family tooling beside the family audit, linted and
type-checked by the same job.

## Options considered

- Relying on the children to report was refused as the standing state of
  affairs, because each such report costs a project a re-alignment and, once,
  a renamed record whose citation now points nowhere.
- Rehearsing by hand before each law change was refused, because a step a
  person must remember is a preference, and the two hand rehearsals this
  week happened only after the reports.

## Consequences

A check has to work in a lived-in tree before it lands. The first run found
a defect of its own: a fresh inquiry could not pass its audit, because the
host's rulebook and guide named the review and arrow folders as paths a
project without a pass or an arrow does not have, and Quiver record 0034
answers it. The rehearsal will not catch what no one has thought to shape
into the child, and each new
class of defect a project finds adds its condition to the child, the way
each leftover class became a named negative in the audits.
