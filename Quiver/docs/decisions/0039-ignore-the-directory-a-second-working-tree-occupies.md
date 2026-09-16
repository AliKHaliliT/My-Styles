# 0039. Ignore the directory a second working tree occupies

Status: Accepted
Date: 2026-09-16

## Context

The branch protocol gives every session its own working tree and says
nothing about where that tree lives. A worker who creates it inside the
repository, under a conventional directory or where its harness puts one,
has made a nested checkout, and git treats such a directory as an embedded
repository, so a careless add records a pointer to it and a status shows
it as untracked until then. No ignore file in the family named such a
directory, and the baseline, which lists what is never tracked, did not
mention working trees at all. Treasury study 0005 found the guard stated in
the published agent-skills ecosystem as the first step of creating a
working tree, verify the directory is ignored and add it if not, and the
family disposition, treasury 0030, Take eight rules from the skills study
and refuse the rest, adopted it as an ignore entry, a baseline row, and an
audit line.

## Evidence

Every seat's ignore file was read on 2026-09-16 and none named a
working-tree directory; the family repository's own ignore file named
editor directories and operating-system files only. The harness in use
creates its working trees under `.claude/worktrees/`, and the published
convention the study read uses `.worktrees/`. The docs audit already holds
root files to the baseline through its rooms check, and the baseline
already lists editor directories as never tracked for the same reason a
working tree is, that what one machine needs is not what the repository is.

## Options considered

- Naming only the harness's directory. Refused, because the guide is
  vendor-neutral and a child may run under a different harness; the
  convention directory is named first and the harness directory beside it,
  the way the ignore file names two editors.
- An audit check that walks the worktree list and verifies each tree inside
  the root is ignored. Refused for now, because it needs a working tree to
  plant, which the selftest cannot create without touching the repository's
  own worktree registry; holding the ignore file to its two lines is
  decidable, plantable, and catches the same mistake earlier.
- Leaving it to the branch protocol's reader. Refused under the ladder,
  because a check can decide this question and no check did.

## Decision

Every seat's `.gitignore`, the family repository's, and the arrow's carried
copy gain a Working trees section naming `.worktrees/` and
`.claude/worktrees/`. Every seat's baseline lists the directory a second
working tree occupies under Never tracked, with the reason. The branch
protocol's bullet in every guide says where a tree created inside the
repository lives. The docs audits and the host audit hold the ignore file to
the two lines, each with a plant that removes them and watches the finding
fire. The rule lands as a check, because nothing can make an unignored
nested checkout impossible, and a check decides it.

## Consequences

A session that creates its working tree inside the repository creates it
ignored, and a child whose ignore file loses the lines fails its docs audit
with the line to restore. Three audits gain one check and one plant each.
The family repository's ignore file, which carries no audit, is held by
review.
