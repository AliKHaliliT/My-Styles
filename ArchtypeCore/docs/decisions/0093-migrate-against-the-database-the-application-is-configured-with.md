# 0093. Migrate against the database the application is configured with

Status: Accepted
Date: 2026-10-08

## Context

`alembic.ini` named `sqlite:///./test.db` and the Alembic environment
read it, while the application reads `DATABASE_URL` from its settings.
The two agreed on the demo's default by coincidence, both ending in the
same file, and parted the moment a deployment named any other database.
The migrations then created and migrated `test.db` beside the
application, which started against a database with no tables. The
settings already offered `database_url_sync` for a synchronous tool,
but nothing called it and it rewrote only the PostgreSQL driver, while
the seat's own example names the SQLite async driver, which a
synchronous engine cannot open. A project built from a host style with
an arrow of this seat reported it on 2026-10-07 after a migration
created `test.db` beside the file its `DATABASE_URL` named.

## Evidence

Measured on 2026-10-08 in a scratch copy of this seat. With
`DATABASE_URL` naming `sqlite+aiosqlite:///./other.db`, generating a
revision and running `alembic upgrade head` under the change below
created `other.db` holding the demo's three tables and the version
table, and `test.db` never appeared. The suite's three new cases hold
the helper to both async drivers and to a URL carrying none.

## Options considered

- Keeping a URL in `alembic.ini` and asking a deployment to set both.
  Refused, because two settings that must agree is the defect itself,
  and the container's entrypoint runs the migrations with no chance to
  edit the ini.
- Reading `DATABASE_URL` in the environment directly and stripping the
  driver there. Refused, because the settings already own the rewrite
  for synchronous tools and a second copy of the rule would drift.

## Decision

The Alembic environment sets its URL from `settings.database_url_sync`,
offline and online alike, and `alembic.ini` names no URL and says where
the URL comes from. `database_url_sync` strips the SQLite async driver
as it strips PostgreSQL's, so the example's own URL migrates, and the
suite holds it to both drivers and the passthrough. The example says
the one URL is read by the application and by its migrations alike.

## Consequences

One setting names the database for the application and its migrations.
A deployment that names another database migrates that database, and a
database with no tables can no longer be the one the application starts
against.
