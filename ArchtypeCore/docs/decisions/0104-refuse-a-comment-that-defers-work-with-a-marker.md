# 0104. Refuse a comment that defers work with a marker

Status: Accepted
Date: 2026-10-15

## Context

Debt lives in STATE.md, one dated entry per shortcut, and the gate says
every shortcut taken is written there before delivery. A comment reading
TODO, FIXME, XXX or HACK is the same shortcut written where the sweep
never looks, a promise beside the code it defers, undated, unqueued and
scrolled past by every reader after the one who wrote it. Nothing in the
backend seat refused one; the tree happened to hold none. A review
method the owner keeps outside the family scans a finished document for
exactly these leftovers, and for the phrases a model writes to a person
rather than for the work, before anything goes out.

## Options considered

- A sentence alone. Refused, because a rule that lives only in a
  sentence binds only a reader who already agrees with it, and a linter
  decides this one whole.
- The markers as advisory. Refused for code, because a marker in a
  comment is decidable and a check that can gate and does not is a check
  that teaches the marker is tolerated; kept as advice for prose, where
  the audit's vocabulary advisory reads an honest use the same as a
  tell.

## Decision

A comment that defers work with a marker is refused by the linter,
ruff's FIX rules selected in `pyproject.toml`, and the rulebook's Prose
section, one text across the family, names the five markers and says the
work goes to STATE.md with its date or to a decision record where the
reason would be lost. The vocabulary advisory in every audit and in the
root workflow names the markers in living prose and, beside them, a
model's leftovers, "As an AI", "as a language model", "I hope this
helps" and "Certainly!", because a sentence a model wrote to a person is
not a sentence written for the project. The tree held no marker, so the
gate landed green and prevents. The rule took the strongest form its
mistake allows, a lint rule for code and an advisory for prose.

## Consequences

Deferred work has one home the sweep reads, and a marker that reaches
the tree fails the gate on the day it is written.