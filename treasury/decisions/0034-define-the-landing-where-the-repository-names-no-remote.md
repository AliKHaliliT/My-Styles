# 0034. Define the landing where the repository names no remote

Status: Accepted
Date: 2026-09-18

## Context

Ruling 0031 left one question to the owner. The branch protocol pushes a
branch, waits for its run, and deletes the branch on the remote in the push
that moves main, and the measured child had no remote, so its worker
committed to main and its workflow never ran. The owner chose the local
form over requiring a remote and over silence, and asked that the local half
of the deletion rule become a check rather than a promise.

## Decision

Without a remote the branch is still merged with main, gated whole in the
terminal, fast-forwarded, and deleted, the push and the wait dropped. Every
docs audit fails while a local branch beside main and the ones checked out
is already merged into main, which holds the local half wherever the audit
runs, and names the workflow's landed-branches step as not run where the
repository names no remote, so the one check that cannot run there is
stated rather than assumed away. The rehearsal's child, which has no remote,
proves both. Requiring a remote was refused as putting hosting inside the
style's jurisdiction; silence was refused as a passing signal. The records
are Keel 0073, ArchetypeCore 0070, Helm 0074, and Quiver 0049, the arrow
inheriting Keel's.

## Consequences

The question 0031 opened is closed. A project with no remote runs the whole
gate in its terminal and lacks exactly the check whose subject does not
exist for it, and a stale local branch goes red in every project.
