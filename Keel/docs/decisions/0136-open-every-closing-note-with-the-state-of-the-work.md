# 0136. Open every closing note with the state of the work

Status: Accepted
Date: 2026-11-24

## Context

The guides name the closing note in three rules, each fixing one thing
it carries, a sending proposed as a numbered option, a file a tool cut
short, and the upstream entries a delivery added. None says how a note
tells the owner where the work stands. The style's owner reported that
with work of several steps, above all work that runs for a while, a note
did not always show whether a task had finished, was still running or
waited on the owner, and asked for a clear signal of the state of the
work.

## Evidence

Read on 2026-11-24 at a2c2cea. The draft rule was read back through a
weaker model with six situations, a branch whose run had just started, a
landed fix whose reporter still had cleanup of its own, a red gate
needing a choice, an answer that changed nothing, a finished feature
beside a stale state entry, and a built change whose landing waited for
the owner. The first reading wrote a done line for the plain answer,
handed the stale entry to the owner as an open item, and could not tell
whether the rule's closing words named a fourth state. The rule was
rewritten in a more decidable form and read back again with a seventh
situation, work both running and waiting, and every situation came out
in the state intended.

## Options considered

- A check of the state line. Refused, because a closing note is a
  message the repository never holds, so no tool can read it.
- A sentence about the state in the worker's own words. Refused, because
  the owner finds the state at a glance only when it takes one of a few
  fixed forms.
- A state line on every message. Refused, because an answer that only
  reads and explains has no work whose state could be in doubt, and a
  line on it would teach the reader to skip the line.
- Listing every step the task took. Refused, because the length buries
  the state, and a self-report of steps proves nothing, the ground on
  which the family refused asking a note to name the documents read
  whole. A state line differs from that self-report, since the owner can
  check it against the tree and the runs, and it orients rather than
  proves.

## Decision

Every closing note, the message that ends or pauses a task, opens with
one state line, and an answer that only reads and explains carries none.
The line takes one of three forms. Done means nothing the task asks of
the worker is left, and it is followed by Nothing pending, or by each
item someone else still holds, with its holder. Waiting on you names
what the work needs from the owner before it can go on, with any
numbered options in the body. Running names what the work set going and
is still running, a gate, a CI run or a background command, and promises
a report when it ends, and a note never says done while one runs. Work
that both waits and runs says both, the wait first. No tool can read a
closing note, so the rule is held in review.

## Consequences

The owner reads where a task stands from the first line of its note. A
long task's notes say Running until its last run reports, and the note
that ends it says Done and names whatever anyone else still holds. A
note without its line, or one that says done too early, is a finding for
review.
