# 0141. Hold each part of the timestamp fix by a case of its own

Status: Accepted
Date: 2026-11-23

## Context

The record that landed the timestamp fix named the cases that held it
and the thirteen breaks they caught. A project built from this style
re-aligned to that commit, proved the suites it took one change at a
time, and found three breaks that passed every case. Each schema's
refusal sent one field without an offset, so the other field could take
a naive stamp unseen, in the API and in the domain alike. The renderer's
case called it directly and no case generated a revision, so the
migration environment could stop handing it to Alembic, after which the
next revision generated for a new model failed when applied. The project
sent the case as an entry.

Breaking the fix one point at a time on the template found two more.
Nothing held the column's request for the time zone. The renderer the
environment passed in its offline mode was never used, since Alembic
generates a revision only over a connection, though the record that
landed the fix said both modes passed it.

## Evidence

Run on 2026-11-23 at 6c9473b with the seat's development requirements.
Under each of the entry's three breaks the seat's 56 cases passed, and
the entry's controls, the field each refusal does send, failed one case
each. With the environment's online pass removed, a revision generated
from the models named `db.types` six times and stopped with a
`NameError` when applied. With its offline pass removed, the revision
came out as before. With the column stored as a DateTime without the
time zone, the 56 cases passed, while the type compiled for PostgreSQL
went from `TIMESTAMP WITH TIME ZONE` to `TIMESTAMP WITHOUT TIME ZONE`.

## Options considered

- Asserting that the environment's text names the renderer. Refused,
  because a check of the text holds the words and not the revision
  Alembic writes.
- Keeping the offline pass for symmetry. Refused, because a line nothing
  runs reads as if it held something.
- Generating the revision against a database a deployment uses. Refused,
  because the suite reaches no database beyond SQLite in memory, and a
  revision rendered over a database with no table names every stamp the
  models declare.

## Decision

Each schema's refusal runs once for each field, that field sent without
its offset and the other with one. A case copies the migration
environment into a folder that holds no revision and runs no write hook,
generates a revision from the models over the suite's database, which
holds no table, requires that it names the stored type once for every
stamp the models declare and nothing of the application's types, and
then applies it. A case compiles the column for PostgreSQL and requires
a timestamp with its time zone. The offline pass leaves the environment,
and the renderer's docstring says the online mode passes it. The ledger
gains the claim that a revision generated from the models applies as
generated.

The fix was then broken at each point on its own, twenty-one breaks over
the type's two functions and its renderer, each column, each field of
each schema and the environment's wiring, and each failed the suite, the
entry's three among them. With the whole fix reverted, the round trip
failed on its assertion. The type's flag that it is safe to cache is
held by the warnings gate, which fails the suite on the warning the
library raises without it.

## Consequences

A project that generates its first revision gets one that applies, and
the suite says so before the project tries. A field added to a timestamp
schema is refused in a case of its own once the case's list names it.
