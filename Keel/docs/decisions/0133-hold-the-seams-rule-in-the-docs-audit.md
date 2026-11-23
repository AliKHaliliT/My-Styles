# 0133. Hold the seams rule in the docs audit

Status: Accepted
Date: 2026-11-23

## Context

The testing rule replaces a collaborator only at a declared seam, and
never by patching a module's internals. A grep over the suites held it,
a step in the workflow each style carries, and the invariants ledger
named that workflow as the claim's holder at the rung impossible. A
workflow runs only at a repository's root, and only where the repository
names a remote. In a project kept inside another, as a client in a
folder of its server's repository, the carried workflow runs nowhere,
and the rule that admits such a project has its adopter run the commands
of its guide, which never listed the grep. A project built from the
client style met it while writing the ledger of a client adopted in a
folder of a server, and sent the case as an entry.

## Evidence

Read on 2026-11-22 at afffa40. The grep stood in six workflows, four
times in the family's own and once in each of the other five, each
style's own and the copy the arrow carries, the host's job for its arrow
among them, and in no guide's commands and no edition's workflow. A
project with no remote never ran it. In the arrow the family keeps, the
ledger's holder was the workflow the arrow carries, a file that has
never run, while the host's job ran the grep in its stead.

## Options considered

- Naming the root's workflow in a nested project's ledger. Refused,
  because the holder would be a file outside the project's tree, which
  its ledger cannot name and its audit cannot read.
- Adding the grep to each guide's commands. Refused, because a command a
  worker must remember is weaker than a check the Docs command already
  runs.
- Keeping the step in the workflows beside the audit. Refused, because
  two holders of one claim drift apart, as the carried workflow's step
  and the root's could.

## Decision

Each artifact style's docs audit holds the rule. It reads every tracked
file under `tests/` outside a project kept inside it, and fails a line
that patches a module, with the patterns the workflow's step used,
`monkeypatch`, `unittest.mock`, `mock.patch` and `MonkeyPatch` in the
Python styles and `vi.mock(` in the client style. The step leaves every
workflow, the family's and each style's, since the Docs step that runs
the audit stands in each of those jobs already. The ledger's row names
the audit as its holder, at the rung impossible. The selftest plants a
patched module under `tests/` and requires the finding, and the check
was broken seven ways across both stacks, among them reading nothing,
reading every file and losing either kind of patch, and each break
failed its proof. This supersedes the record that carried the grep in
the workflow a project inherits.

## Consequences

The rule holds wherever the gate's Docs command runs, in a project with
no remote and in a project kept inside another, whose own audit reads
its suites. A suite that patches a module fails the docs audit by file
and line. The landing step is again the one check a workflow carries
beyond the gate's commands, as the audit's report of a missing remote
already says.
