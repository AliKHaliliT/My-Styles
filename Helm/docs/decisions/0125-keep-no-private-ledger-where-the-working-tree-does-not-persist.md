# 0125. Keep no private ledger where the working tree does not persist

Status: Accepted
Date: 2026-11-19

## Context

The baseline gives a private fact one home, the untracked `LOCAL.md` at
the root, and the rules of conduct tell a worker to read it when it
exists and to create it when first needed. The record that chose the
file chose it because it persists on the machine, and refused a scratch
file that dies with its session, since a later session would then ask
the owner again or derive the fact afresh and leak it. A hosted agent
session works in a sandbox that is rebuilt from the repository once it
has been reclaimed, so a `LOCAL.md` written there is the file that
record refused. It vanishes without a trace, and the next session reads
its absence as nothing having been withheld. A project built from hosted
sessions ruled that its sessions keep no such file, and sent the case as
an entry.

## Evidence

Read on 2026-11-19. In no seat does the rule or the baseline name a
worker whose tree does not persist. The documentation of the sessions'
provider says that a session starts from a fresh clone of the
repository, that what is committed there is what is available, and that
reopening a session whose paused machine has been reclaimed provisions a
fresh one.

## Options considered

- Keeping the file in the sandbox and copying it out of the repository
  after every change. Refused, because a copy sent out is a sending the
  rules of conduct reserve to the owner, and the ledger's survival would
  hang on a step taken after every edit.
- Keeping the file in the sandbox and accepting its loss. Refused,
  because the loss is silent.
- Leaving the case to each project. Refused, because the rule tells a
  worker to create the file, and a worker in a sandbox that obeys it has
  lost the fact by the next session.

## Decision

Where the working tree does not outlive the session, no `LOCAL.md` is
created. The tracked entry carries the public-safe version, and its
pointer says the owner holds the fact. The worker puts the private fact
to the owner in the conversation, the owner keeps it outside the
repository, and a session that needs a fact asks the owner for it. On a
machine that keeps its files the baseline stands as written. The rules
of conduct and the baseline both say so, in words read back through a
weaker model before they landed, which asked what the pointer says where
no file stands. The rule is held in review, since the file is untracked
by design and no check in the tree can see what a session wrote outside
it or where a session runs.

## Consequences

Nothing private depends on a sandbox surviving, and nothing private
leaves the repository by an agent's hand. The owner carries the ledger
for such sessions, which costs a question whenever a session needs a
fact another was given.
