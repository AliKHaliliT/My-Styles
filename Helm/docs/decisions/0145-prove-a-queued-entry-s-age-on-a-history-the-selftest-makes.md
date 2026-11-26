# 0145. Prove a queued entry's age on a history the selftest makes

Status: Accepted
Date: 2026-11-26

## Context

A queued, deferred or blocked entry that stands for two horizons with
its text unchanged fails the audit, its age read from git's history and
counted from the rule's own arrival where the entry is older. The
selftest proved the rule on nothing. No plant can give this tree's
history an old entry, so the selftest printed that the firing case was
skipped, on every run and in every tree, without looking for an entry to
run it on. A project built from the host style reported it, having
proven the rule itself in repositories of its own with dated commits.
Planting an age at its edge then showed that this audit counted days by
the clock.

## Evidence

Run on 2026-11-26 at 6a35476. The selftest's skip line stood after the
state plants with no condition on it. A copy of the audit, run whole in
a repository holding only itself and a state file, with commits dated
181 and 180 days back, named the older entry as standing 181 days and
not the younger. The audit read a date as local midnight and divided the
elapsed time by a day, and on Linux, under two zones that keep daylight
saving, that count from a day in May to one in November came to 181 at
half past ten at night and 182 an hour later, and across the spring
change it came to 180 in the first hour of the day and 181 after it.
Under a zone that keeps none it came to 181 at every hour, as the
calendar does.

## Options considered

- Passing the check a history to read in place of git. Refused, because
  the reading of git's history is half of what the rule does, and a
  proof that feeds the check its answers proves the other half alone.
- Keeping the named skip. Refused, because a rule with no firing proof
  and a rule that cannot fire look the same.
- Planting the ages away from their edge, as the state plants do, and
  leaving the count as it stood. Refused, because the edge is where the
  rule decides, and a count that turns a day an hour early or late is
  wrong for the audit's reader as well as for its proof.

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
the day turned while it ran. The audit now counts the days from a date
to today by the calendar, for a state entry's date, an entry's standing
and an upstream entry's date alike. On Linux, eight breaks, each one
point, each failed the proof. A ninth, the count by the clock put back,
survived, since the hour in which it differs cannot be planted.

## Consequences

The rule's threshold, its exemption for work in flight, its reading of
an entry's first day and its limit at the rule's arrival each have a
proof behind them, and the selftest prints no skip for them. An age read
on a machine that keeps daylight saving is the calendar's at every hour.
