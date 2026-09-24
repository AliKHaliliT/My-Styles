# 0080. Declare the models' columns with Mapped

Status: Accepted
Date: 2026-09-24

## Context

The three models and the timestamp mixin declared their columns in the
form SQLAlchemy documented before its 2.0 release, a bare `Column(...)`
assigned to a class attribute. That form kept working, and the type checker
read each attribute loosely enough that comparisons in the repositories
passed. SQLAlchemy 2.1.0 was released on 2026-09-24, between two runs of
the build a few hours apart, and its typing reads a bare column on a
declarative class as an attribute of no type at all. Every ordered
comparison in the user repository collapsed to a plain boolean, the query
builder refused it, and the type check went red on a file no change had
touched. The same release stopped installing `greenlet` on its own, so the
asynchronous session the seat runs on failed to import unless the
`asyncio` extra is named.

## Evidence

The last green run installed SQLAlchemy 2.0.54 and the red one 2.1.0, with
the same mypy. Reproduced in a fresh environment with the seat's development
requirements. The revealed type of a model column accessed on the class is
`Never` under 2.1.0, and four comparisons in the user repository fail as the
build reported. The three models hold thirteen columns and two relationships
between them, and the mixin two more.

## Options considered

- Pinning SQLAlchemy below 2.1. Refused, because the template teaches the
  form its dependencies document today, and a pin defers the same change to
  every project built from it.
- Silencing the four lines. Refused, since the checker was right that the
  attribute had lost its type.
- Typing only the compared columns. Refused, because a model that mixes the
  two forms teaches neither.

## Decision

Every column is declared as `name: Mapped[type] = mapped_column(...)`, and
every relationship as `Mapped[...]` of the related class, imported for the
checker alone. The columns' arguments do not change, so the schema and the
migrations do not change. The requirements name `sqlalchemy[asyncio]`, the
install target the library now requires for its asynchronous session. Under the ladder this is the form the seat's own
tooling now refuses to do without, held by the type check that went red.

## Consequences

The type check is green under 2.1.0 and under 2.0. A project built from
this template meets the same release the next time its dependencies
resolve, and its models are its own, so it takes the form from this record
rather than from a recopy. The seat's dependency list stays unpinned.
