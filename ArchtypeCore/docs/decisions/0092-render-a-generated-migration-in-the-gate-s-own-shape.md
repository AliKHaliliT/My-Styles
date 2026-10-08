# 0092. Render a generated migration in the gate's own shape

Status: Accepted
Date: 2026-10-08

## Context

The seat ships Alembic's own script template under `db/migrations/` and
no revision, so the first `alembic revision --autogenerate` a project
runs is the first time the template is rendered, and what it renders is
Alembic's shape, not this seat's. The header imports `typing.Union` and
`typing.Sequence`, which the lint's `UP` codes refuse, `upgrade` and
`downgrade` carry no docstring, which `D103` refuses, the file opens
with a module docstring, which the rulebook allows to a script run as a
command and to nothing else, and Alembic writes the operations with
single quotes, which the `Q` codes refuse. A project built from a host
style with an arrow of this style reported on 2026-10-07 that its first
generated revision raised 205 findings while the type check passed.

## Evidence

Measured on 2026-10-08 in a scratch copy of this seat. The first
revision generated from the demo's three tables raised 62 findings,
56 of them `Q000` on Alembic's quotes, three `UP007`, two `D103` and
one `UP035`; mypy passed. With the template below and a post-write
hook running `ruff check --fix` over the file Alembic writes, the same
generation raised nothing, the hook reporting 56 fixed and none
remaining, and mypy passed again.

## Options considered

- Carrying the rewritten template alone and naming a `ruff check --fix`
  step beside the command, as the project proposed. Refused, because
  the quotes come from Alembic's rendering, which no template reaches,
  and a step a person remembers is the weakest form a rule can take.
- Excusing generated revisions from the quote and docstring codes in
  the lint's per-file ignores. Refused, because a revision is read and
  edited by hand after it is generated, and a file the gate cannot read
  is a file the gate does not hold.

## Decision

The script template renders a revision in this seat's shape. It opens
with a comment header carrying the message, the revision identifiers
and the date, types the identifiers with PEP 604 unions and
`collections.abc.Sequence`, and gives `upgrade` and `downgrade` each a
one-sentence docstring in the house rhythm. `alembic.ini` names ruff as
a post-write hook that runs its fix over the file Alembic writes, so the
single quotes Alembic renders are rewritten before anyone reads them,
and ruff comes with the development requirements, where generating a
revision belongs. The agent guide names the generate command beside the
migrate command.

## Consequences

The first revision a project generates passes the gate as written. A
generation without ruff on the path fails loudly at the hook, which is
the right failure, since a revision generated without the tooling is
one nobody has linted.
