# 0031. Make the shapes copyable and the questions answerable

Status: Accepted
Date: 2026-09-10

## Context

A week of upstream traffic showed one pattern in every misreading: a rule a
strong reader resolved by intent, a weaker one resolved literally, and an
ambiguity that was real either way. Each was fixed by making the rule
decidable, never by lowering the text. Three places remained where the family
still asked a reader to interpret rather than copy or choose. The upstream
entry's shape lived in one prose paragraph, because the demo child honestly
has nothing open and so carries no entry to cut from. A question an agent
puts to its owner, in a pause or in a closing note, had no form, so a
free-form answer to a free-form question was interpreted, and interpretation
is where the weaker model slips. And a scratch clone into a deep Windows
folder failed to check out a record whose filename ran to ninety characters,
because the rulebook says "short-kebab-title" and nothing had ever held
short.

## Decision

The upstream section carries the entry's shape as a fenced block, bytes to
copy rather than a sentence to interpret. A question to the owner is posed as
numbered options, each stating in one sentence what the agent will do if it
is chosen, with the recommended one marked, so the answer can be a number or
a word; a reply that matches no option is restated in one sentence at the top
of the next message, as what was understood and is about to be done, before
anything is done. A record's filename stays within seventy-two characters,
and the audits hold the cap for records added after the rule arrived, binding
from its scope sentence like every history-reading check, so no existing
record is judged and none is renamed.

## Options considered

- Lowering the register of the law for weaker readers was refused, as it
  always is; every fix here adds a decidable form and removes nothing a
  strong reader uses.
- Renaming the long records was refused, because records are immutable and
  their names are how they are cited; the cap binds forward.
- A gate item requiring a comprehension test of every law change by a weaker
  model was refused, because a gate that cannot run in the family's CI is a
  preference in a gate's clothing; the read-back stays a drafting practice.

## Consequences

An agent writing its first upstream entry copies a shape. An owner answering
an agent answers with a number, and sees a misreading in a first line rather
than in the work. A record written from today fits a Windows path.
