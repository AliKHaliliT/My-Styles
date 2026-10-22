# 0112. Withhold a link's target and a path beyond a symbolic link

Status: Accepted
Date: 2026-10-22

## Context

Record 0106 made a recorded artifact the ignore file names no verdict,
named on every run as a check not run. The audit asked git whether the
path is ignored, and git refuses to judge a path that passes through a
symbolic link, so an artifact kept on removable storage behind an
ignored link read as unignored and failed as a path the tree does not
hold, and the verdict changed with the storage plugged in or out, though
neither the index nor the ignore file had changed. A relative link whose
target the ignore file covers was still a dead link, a verdict on a path
the tree cannot hold. A project built from this template met both at
once.

## Options considered

- Follow the link to decide custody. Refused, because what a link points
  at on one machine says nothing about the tree, and the audit judges
  the tree.
- Leave relative links as verdicts and let a project avoid linking
  withheld files. Refused, because the family's own rule for a withheld
  artifact is that no checkout can vouch for it, and a link to it is the
  same claim in another form.

## Decision

A path git refuses to judge is judged by the nearest ancestor git
answers for, because the ignore rule that covers a link covers
everything reached through it; the link itself is never followed. A
relative link whose target the ignore file covers is no verdict either
way; the dead-link check passes it over and the not-run list names it,
for the living documents and the records of the project's own alike,
with whether the target lies on that machine. The selftest plants a
withheld link, absent and present, and a recorded artifact behind an
ignored symbolic link where the machine can make one. The freshness
bullet and the claims rule say so.

## Consequences

A withheld artifact reads the same whether it sits in the tree's folders
or behind a link, a link to it stops failing on the machines that lack
it, and the ignore file stays the one declaration that withholds.
