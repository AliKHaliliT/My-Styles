# 0131. Cut a public edition by tier and by version

Status: Accepted
Date: 2026-11-10

## Context

The baseline has every tracked byte written for a public audience, so a
project built from a style can be published as it stands. Nothing served
the owner who wants the product public and the workshop kept back, the
records, the rules and the gates, which together are the method.
Publishing by hand meant choosing paths one by one and rewriting a
README whose schema points at the rulebook, and a hand that misses a
line publishes the pointer. Measured on 2026-11-09 over the four seats,
the style and its trail are 140 to 180 of each seat's 210 to 360 tracked
files and separate by path, and what remains names the style in about
twenty lines a seat, in the comments of the tool configuration, in the
workflow and in a few comments that cite a record.

## Options considered

- Shed the workshop by degrees, a tier with the records and no rules,
  another with the rules and no state. Refused, because a commit message
  cites a record, a record cites the rulebook and the records it
  inherited, the invariants ledger names the audits, and history holds
  every file that was ever tracked, so a part cut alone leaves the rest
  pointing at nothing. The snapshot is the one step that stands, history
  alone.
- A lean tier between the hand-made and the bare, the code as written
  under a README cut short. Refused, because it differs from the
  hand-made tier by a shorter page and a missing workflow, and a tier
  costs a definition, its proofs and a place in every seat. It reopens
  when a project needs code as tested with nothing to read.
- Have the tool reword whatever names the style. Refused beyond a
  comment, because a docstring and a document are what a product says of
  itself, and a tool that rewrites them publishes words nobody wrote.
  The cut refuses, and the owner rewords the line where it is written.
- Strip every kind of file at the bare tier. Refused, because a strip is
  trusted only through a proof, and a kind with no parser at hand to
  give one is carried as written and named. It reopens for a kind when a
  parser the project already installs can prove its strip.
- Carry history below the snapshot by rewriting it. Refused, because
  history holds every file that was ever tracked and its messages cite
  records, so no rewrite leaves it both true and silent.

## Decision

A project is published at one of four tiers. The whole tier is the
repository itself. The snapshot is every tracked file as one new commit.
The hand-made tier, the one to reach for, is the product as written with
no record, no rule and no gate in it. The bare tier is the hand-made
tier with comments and docstrings stripped and a README cut to what the
thing is and how to run it. Below the snapshot a tier is cut in two
versions, an attributed one that names the template and its tier, and a
silent one that names nothing of the style. What names the style is a
closed list, the family by its name, a record by its number and a
withheld path by its name. A silent cut drops a comment that names the
style with its block, cuts the sentences of the README's opening that
name the family, and refuses on a docstring or a document line, which is
then reworded in the workshop. The tier and the version are the owner's
to name, and a cut asked for no version is attributed.

The edition tool carries this out. It cuts from the last commit,
assembles the edition whole before it writes a byte, writes into an
empty folder outside the repository, refuses a destination under which a
path would run past what the system is sure to write, and never commits,
pushes or deletes, because publishing is the owner's. A project kept
inside another is cut by its own tool, so the edition of an inquiry is
its arrows. Files the public receives in another form live under the
edition folder's overlay, the plain workflow first, and a project's own
withholdings in its list. The editions document states the law, the
guide lists the two commands, the baseline gives the folder its trigger,
the adoption document carries the document and the tool at re-alignment,
the invariants ledger takes two rows, the workflow runs the tool's
selftest, and the docs audit holds the overlay's workflow to the pins it
holds every workflow to.

A strip is trusted only through its proof, a parse of the source against
a parse of what is left. The tool's selftest cuts a project of its own
making at every tier and in both versions, and each of its proofs was
watched failing on a break of the tool before it was trusted,
twenty-seven breaks of the one text the Python seats carry and
twenty-six of the client seat's, none surviving. Cut from the demos on
2026-11-10, the bare tier passes each suite it was cut from, twenty-five
tests in the package seat, forty-six in the server seat, twenty-three in
the client seat and twenty-one in the arrow, and the server seat's
interface loses the description of all thirteen of its operations, which
were its docstrings.

## Consequences

An owner publishes the product and keeps the method, by one command and
with a check that the pointer is gone. A bare edition is for running and
not for reading, since it passes its tests and not a lint that demands
docstrings. A template cannot be silent about itself, so the silent
version is proven on a project the selftest builds and never on a demo.
