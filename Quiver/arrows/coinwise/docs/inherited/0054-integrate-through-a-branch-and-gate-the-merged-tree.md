# 0054. Integrate through a branch and gate the merged tree

Status: Accepted
Date: 2026-09-15

## Context

The owner asked what happens when two sessions work on one project at once,
when both write the next record number, when the second push is refused, and
when an agent finds the tree changed under it. Two sessions in one working
tree break everything, because the host audit's selftest plants defects and
rewrites living files for seconds at a time, and the other session sees a
planted tree and may commit it. With a worktree each, every collision the
tools can see ends in a red run that names its cause, two records sharing a
number, a pin a rebase rewrote, a link that no longer resolves. Three habits
stayed unnamed by the law: the gate was not rerun after a merge or a rebase,
though the commands item already says the final tree; a pin could name a
commit a later rebase would rewrite; and an agent that saw a change it did not
make read it as its own error and repaired it, which is how two agents undo
each other's work. The owner proposed working on a branch and integrating at
the end with a look at what had happened since.

## Options considered

- Keep committing straight to main and let CI catch the merged result.
  Refused. The red lands on main for everyone, and nothing names the moment
  to look at what changed.
- Rebase onto main as the integration step. Refused, because a rebase
  rewrites the commits that records and manifests pin, and the pin then
  names a commit the history no longer holds.
- Detect another session by inspecting the tree. Refused. A session cannot
  tell a tool's edit from a session's, and does not need to; what it can
  tell is an act it did not perform, and that is enough to stop and ask.
- A lock or a central counter for record numbers. Refused. No mechanism
  reaches across sessions, and the audits already report a shared number by
  both filenames with the fix in the message.

## Decision

One working tree and one branch per session, never two sessions in one tree.
A change lands by merging main into the branch, running the gate on the
merged tree, pushing the branch, waiting for its run to pass, and
fast-forwarding main, so main never carries a tree the gate has not seen
whole. Integration is a merge and not a rebase where records pin commits. The
commands item names the final tree as the tree that gets pushed, so a merge or
a rebase after the last run makes a new final tree and the commands run again
on it. The pause rule gains one trigger: a change in the tree this session did
not make is another actor, a session or a tool, and is reported and left alone
rather than repaired.

## Consequences

A lone session pays about a minute of ceremony per landing and gains a green
run before main moves. Two sessions pay the same and meet at the merge step,
where the audits name every collision they can see and the rerun catches what
the merge changed. Semantic conflicts, two changes that agree with the tools
and disagree with each other, stay review's. The host audit gains the
duplicate-number check the docs audits already had, so a shared claim or
decision number is named at the merge like a shared record number.
