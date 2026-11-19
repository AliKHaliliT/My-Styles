# 0133. Declare a constraint where a generated migration carries it

Status: Accepted
Date: 2026-11-19

## Context

Two of the demo's models, the user and the device, declared the check on
their status inside the column, passed to the column beside its type.
The guide's command for a migration, `alembic revision --autogenerate`,
renders the constraints a table holds and passes over one a column
holds, so the first revision generated from a model cut from these
exemplars creates its table with no check on status. The tables built
from the models themselves carry the check, so two ways of building one
database disagreed, and the weaker is the one a deployment runs. A
project built from this template met it on its first migration, moved
its constraint onto the table under a name, and sent the case as an
entry. The record that moved the columns to their typed form said their
arguments do not change and did not rule on where a constraint is
declared, and the record that put a generated revision in the gate's
shape measured it by its lint findings alone.

## Evidence

Run on 2026-11-19 in a scratch copy of this seat at 05807a1, with
Alembic 1.20.1 and SQLAlchemy 2.1.9 on SQLite. The revision generated
from the demo's three tables held no check constraint. The database
built from it accepted a user whose status the model refuses, and a
database built from the same models by `create_all` refused the row,
naming the check. With the constraint moved onto the table under a name
in both models, the revision carried both checks and both databases
refused the row. In a table built for the purpose, a constraint on the
table reached the revision named or unnamed and one inside a column did
not, and a check added to a table that already existed drew no operation
from the generator at all.

## Options considered

- Leaving the exemplars and telling the reader of the guide to read a
  generated revision against its model. Refused under the ladder,
  because where a constraint is declared is a fact the suite reads in
  one loop, and a sentence would bind only a reader who already knew.
- A test that generates a revision from the models, builds a database
  from it, and compares it with the one the models build. Refused,
  because it would execute rendered code inside the suite to catch the
  one form known to be passed over, which the loop decides without it.
  It reopens when a generated revision is found to pass over a second
  form.
- Naming the constraint through a convention on the metadata. Refused,
  because a convention names a constraint and does not move it, and one
  declared inside a column is passed over under any name.

## Decision

A constraint is declared on the table, in `__table_args__` under a name,
and never inside a column. The two exemplars declare their status check
there, named for the table and the column, and a comment beside each
says why. The suite gains `tests/db/test_base.py`, which reads every
table the models declare and fails while any column holds a constraint
of its own, naming the column, so a model cut in the old form goes red
before its first migration is generated. The test was watched failing
with each exemplar put back in the old form. The invariants ledger takes
the claim with the test as its holder, and the map names the suite.

## Consequences

The first revision a project generates builds the checks its models
declare, and a failed check names its constraint. A project that built a
database from the old form keeps an unnamed check there, and since the
generator proposes nothing for a check added to a table that exists,
such a project writes that revision by hand.
