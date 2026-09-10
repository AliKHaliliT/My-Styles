# 0033. Compare history by ancestry, never by the calendar

Status: Accepted
Date: 2026-09-10

## Context

A project re-aligned and brought in the cap on record filenames. The audit
ran green before the commit that carried the cap, because the scope sentence
was in the working tree and in no commit, so nothing was judged; the next run
failed two claims written earlier the same day. The check read the arrival of
its rule and the addition of each record as committer dates, without a time,
and compared them with a greater-or-equal, so a record committed hours before
the rule compared equal and was judged. The project renamed both claims, and
in a sibling arrow the same defect caught a record that an accepted record
cited, so a citation there now names a path that does not resolve. Worse, the
selftest refused to plant over the red tree and reported three rules not
working, when one filename was long. The immutability check, the oldest
history-reading check, had always walked ancestry and never had this defect;
the two newer ones took a calendar shortcut instead of copying it.

## Decision

Every history-reading check compares commits by ancestry. A record is exempt
from the filename cap when the commit that added it is a proper ancestor of
the commit that brought the rule; added in that commit or after it, it is
judged, whatever the dates say. The queue-age check counts an entry's standing
from the binding commit only when the entry's first commit is a proper
ancestor of it, and from the entry's own commit otherwise. Before means an
earlier commit, because two commits on one day are ordered by the history and
not by the calendar. The selftest checks the tree first and, where the audit
already fails, prints those findings and stops with one line saying nothing
can be proven until the audit passes, instead of running plants that cannot
pass and counting them as broken rules.

## Options considered

- Comparing full timestamps was refused. Clocks disagree across machines, a
  rebase rewrites committer times, and the question was never when but
  whether one commit came from the other.
- Leaving the selftest's refusal as it stood was refused, because a command
  whose purpose is to show that the checks fire must not say three rules are
  broken when it means the tree is red.

## Consequences

A rule that arrives never reaches behind its own commit, on the day it lands
or any other. A red tree is reported as a red tree. The reporting project's
renamed claims stay renamed, and its broken citation is the last one this
defect makes.
