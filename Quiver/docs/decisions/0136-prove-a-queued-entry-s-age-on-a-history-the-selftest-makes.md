# 0136. Prove a queued entry's age on a history the selftest makes

Status: Accepted
Date: 2026-11-26

## Context

A queued, deferred or blocked entry that stands for two horizons with
its text unchanged fails the audit, its age read from git's history and
counted from the rule's own arrival where the entry is older. The
selftest proved that an entry written today passes and nothing more. No
plant can give this tree's history an old entry, so the selftest printed
that the firing case was skipped, on every run and in every tree, though
its own description said the case runs where a tree carries such an
entry. A project built from this template reported it, having proven the
rule itself in repositories of its own with dated commits.

## Evidence

Run on 2026-11-26 at 6a35476. The selftest's skip line stood after the
fresh entry's plant with no condition on it and no search before it. A
copy of the audit, run whole in a repository holding only itself and a
state file, with commits dated 181 and 180 days back, named the older
entry as standing 181 days and not the younger, so the audit runs whole
where a proof can date the commits.

## Options considered

- Passing the check a history to read in place of git. Refused, because
  the reading of git's history is half of what the rule does, and a
  proof that feeds the check its answers proves the other half alone.
- Aiming the audit's git calls at a second repository inside one
  process. Refused, because the audit remembers git's answers for the
  life of a process, so two repositories would share one memory.
- Keeping the named skip. Refused, because a rule with no firing proof
  and a rule that cannot fire look the same.

## Decision

The selftest builds two repositories of its own, each holding a copy of
this audit and a state file, with commits dated at noon of chosen days,
and runs the copy in each as a child process with no variable in its
environment that names another repository. In the first the rule is
older than every entry, and the audit must name a queued entry a day
past two horizons and neither a deferred one a day short nor one in
flight. In the second the entry is older than the rule, and the audit
must count it from the rule's arrival and name nothing. The entries are
committed under their day's date and re-dated on disk, the way an entry
is kept alive without a change of text, and the proof starts over where
the day turned while it ran. The fresh entry's plant in this tree stays.
Eight breaks, each one point, each failed the proof.

## Consequences

The rule's threshold, its exemption for work in flight, its reading of
an entry's first day and its limit at the rule's arrival each have a
proof behind them, and the selftest prints no skip for them. The proof
costs two small repositories and two runs of the audit, about four
seconds at the family's desk.
