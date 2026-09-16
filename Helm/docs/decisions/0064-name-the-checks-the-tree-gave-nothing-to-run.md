# 0064. Name the checks the tree gave nothing to run

Status: Accepted
Date: 2026-09-16

## Context

An audit that ends with the tree agreeing with its conventions has said
what it found, and not what it looked at. Several checks return without a
word when the tree gives them nothing: the STATE check when no STATE file
exists, the upstream check when a template carries no upstream file, the
layout and docstring checks when no package root is on disk, the import
graph check when no contract names its roots. In the template every such
absence is legitimate, and in a project built from it a missing STATE file
or a lost upstream file is a defect, and the same clean line covered both.
The selftests already say which plants they skip and why. Treasury study
0005 found the rule stated in the published agent-skills ecosystem for a
privacy linter, a check that cannot apply says so and every run ends with
the checks that did not run, and the family disposition, treasury 0030,
Take eight rules from the skills study and refuse the rest, adopted it for
the audits.

## Evidence

The audit's run reports its problems, its advice, and the package roots it
held the layout over, and that last item was the one precondition it
already named, printed as layout held over a root or over no package tree.
Every other check with a precondition was silent about it. The docs audit's
own guide says a check may never imply more than it decides, and a verdict
of agreement over a tree where a check never looked implies exactly that.

## Options considered

- Threading a fourth list through every check so each names its own skip.
  Refused, because it changes the signature of every check with a
  precondition and the arity every plant destructures, for a report the
  table beside the run states in six lines.
- Reporting the skips as advice. Refused, because advice is a finding review
  must answer, and a check that did not run is a fact about the tree's
  shape, answered by nothing.
- Failing when a check cannot run. Refused, because the template legitimately
  carries no upstream file and a docs-only child legitimately carries no
  package root; the report is honesty, not a gate.

## Decision

Each audit carries a table of what its checks need, one path or one
declared value per check, and a function that names every check whose need
the tree lacks. The report prints before the advice, gates nothing, and
names the check and its need on one line. The three docs audits name the
STATE, upstream, rooms and docs-zone checks by their files, the layout and
docstring checks by a package root, the import graph check by its contract
roots, and the version-story check by the declared floor; the host audit
names its STATE, upstream, reviews, arrows and pins checks by their files.
Each selftest hides the STATE file, watches the report name the STATE check
as not run, confirms it did not say so while the file was present, and
restores the bytes. The guide's paragraph on report levels gains a third
level, not run, with what it needs. The rule lands as a check on the audit
itself, the second rung; no shape of the audit can make a silent skip
impossible, and the table decides the question on every run.

## Consequences

A project's audit output now says, on every run, which checks its tree gave
nothing to run, so a missing STATE file reads as a named absence rather than
as agreement. The template's own runs name the upstream check, which is
correct, since a template carries no upstream file. The table is the one
place a check's need is stated beside the check that has it, and a new
check with a precondition adds its row in the same change or the selftest's
reviewer asks why not.
