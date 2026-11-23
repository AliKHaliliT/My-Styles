# 0139. Hand a timestamp out of the store in UTC with its offset

Status: Accepted
Date: 2026-11-23

## Context

The timestamp mixin declared its two columns as timezone-aware DateTimes
filled by the database's clock. SQLite keeps no offset, so on the
database the seat's settings name, through the only driver the seat
installs, both stamps came back naive although SQLite wrote them in UTC.
The schemas typed the two fields as plain datetimes, so the API sent a
stamp with nothing to say which zone it stood in, while the examples in
the same schemas read `2026-06-15T12:00:00Z`. A browser reads a stamp
with no offset as its own local time. A project built from this style
met it while cutting a client's wire schema against its server, and sent
the case as an entry.

## Evidence

Run on 2026-11-22 at afffa40, the commit the entry pins, with the seat's
models, its driver and its API schema over SQLite in memory. The stamp
came back as `datetime(2026, 11, 22, 7, 46, 36)` with no offset, equal
to the clock in UTC at that moment, and the schema sent
`"created_at":"2026-11-22T07:46:36"` and the same for the other field.
Read by JavaScript's `Date` in a zone seven hours behind UTC,
`2026-11-22T01:57:35` became `2026-11-22T08:57:35.000Z`, seven hours
late, and the same stamp with a `Z` was read as written.

A revision generated from the models with the new column type named
`db.types.UTCDateTime` six times without importing it, the lint hook
left six errors, and applying it failed with a `NameError` that found no
`db` defined. With the renderer in place the revision named
`sa.DateTime(timezone=True)` six times and nothing of the application,
it applied, `alembic check` reported no new upgrade operation, and a
stamp read back from the migrated database was sent as
`2026-11-23T16:24:29Z`.

## Options considered

- Reviving the stamp as UTC in the client. Refused, because the wire
  would still say nothing of its zone, and every other reader of the API
  would need telling.
- Attaching the offset in each repository translator. Refused, because
  the offset is lost in one place, the column, and every later model's
  translator would have to remember it.
- Adding the suffix as the API serializes. Refused, because the domain
  would still hold naive moments, and whatever in the server compared or
  formatted one would be wrong on a machine whose clock is not set to
  UTC.
- Storing a stamp as text or as a number. Refused, because it would
  rewrite the columns and gain nothing the type does not give.
- Rendering the type into a revision with an import of it. Refused,
  because a revision that imports the application breaks on the day the
  application's code moves, and the database stores a plain DateTime
  either way.

## Decision

A column type in `db/types.py` hands a stamp back aware and in UTC. It
attaches UTC to a moment the database kept no offset for, turns an aware
one to UTC, and refuses to bind a naive one. The timestamp mixin
declares both columns with it. The type reads SQLite and a database that
keeps the offset, and says so in its docstring, since a database that
keeps no offset and writes its own local time is not one it can read.
The domain's and the API's timestamp mixins type both fields as moments
that carry their offset, so a naive moment is refused as either schema
builds it. A renderer beside the type gives Alembic the DateTime the
column stores, and the migration environment passes it in both of its
modes, so a generated revision imports nothing of the application.

The form is listed cases, since the static checker cannot tell an aware
datetime from a naive one. Cases hold the type's two functions and its
renderer, the round trip from SQLite to the bytes the API sends, and
each schema's refusal, and thirteen breaks of the change were each
caught, among them the whole fix reverted, under which the round trip
failed on its assertion. The ledger gains the claim that every timestamp
the API sends carries its offset, held by the round trip.

## Consequences

Every stamp the API sends says which moment it is, and a client's wire
schema can refuse one that does not. A model added later gets the same
from the mixin, and a revision generated for it applies as written. A
moment bound from Python with no offset now raises where it once was
stored silently.
