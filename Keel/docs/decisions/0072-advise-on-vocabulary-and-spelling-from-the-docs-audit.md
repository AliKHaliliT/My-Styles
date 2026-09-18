# 0072. Advise on vocabulary and spelling from the docs audit

Status: Accepted
Date: 2026-09-18

## Context

Two advisories lived in the workflow alone, a grep for the vocabulary the
prose law bans and a spelling pass with codespell, each advisory because an
honest domain term reads the same as a tell and a name reads the same as a
typo. The gate says every advisory that prints is read and then fixed or
dismissed in writing. A project with no remote never runs its workflow, so
in such a project neither advisory ever printed and neither was ever
answered, which the measurement of 2026-09-17 found in a child whose prose
carried slop words nobody had seen flagged. The em dash count had moved
from the workflow into the docs audit the day before for the same reason,
and the ruling that moved it named these two as the next candidates.

## Evidence

The vocabulary grep is one regular expression over the tracked files with
the workflows, the rulebook that lists the tells, and the records excluded,
and it moves into a script without a dependency. The spelling pass needs
codespell, which the workflow fetched with pipx on every run and no seat's
development dependencies carried. The docs audit already names a check it
could not run, so a missing tool has a form to report in. The audit's
proofs run the checks forty times over planted trees, and a spelling pass
that spawns a process each time would cost the selftest the seconds the
family took back on 2026-09-15.

## Options considered

- Leaving both in the workflow. Refused, because a rule that prints only
  where a remote exists is a sentence in a project without one, which is
  the form the ruling of 2026-09-17 refused for the em dash count.
- Installing codespell from the audit. Refused, because an audit that
  fetches a tool over the network to run is a build step in a check's
  clothing, and a tree with no network would then fail a check that only
  advises.
- Running the spelling pass inside the checks the proofs exercise. Refused,
  because forty spawns of an external process per selftest is the cost the
  family measured and removed; the pass runs once per audit command and its
  proof calls it directly.
- Keeping the steps in the inert workflows beside the audit. Refused,
  because a check has one home, and the workflow runs the audit already.

## Decision

Every docs audit advises on the banned vocabulary over the tracked text
files, skipping the workflows, the rulebook, the records, and its own word
list, and advises on spelling by running codespell over the tree with the
workflow's skip list where the tool is on the path, naming itself as not
run where it is not. The vocabulary advisory runs with the checks; the
spelling advisory runs once per audit command, outside the checks the
proofs repeat, and its proof plants a misspelling and calls it directly.
The Python seats add codespell to their development dependencies and the
client and host workflows install it before the audit, so CI still hears
both. The inert workflows lose the two steps, and the family's own root
workflow keeps its copies for the treasury and the root scripts, which no
seat audits, skipping the audit scripts that now carry the list. The
guides' two-levels paragraph names the two as the audit's advisories.
Under the ladder nothing changes rung; both stay advisory, because neither
question can be decided by a tool, and both now run wherever the audit
runs.

## Consequences

A project with no remote hears about a slop word and a misspelling on its
next audit run and answers them under the gate as every other project does.
The audit command takes a moment longer where codespell is installed, and
the selftest is unchanged. A project that has not installed codespell reads
one line naming what it needs and installs it, or lives with the line.
