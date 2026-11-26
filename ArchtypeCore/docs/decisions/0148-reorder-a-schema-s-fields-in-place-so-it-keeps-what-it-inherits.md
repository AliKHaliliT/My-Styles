# 0148. Reorder a schema's fields in place so it keeps what it inherits

Status: Accepted
Date: 2026-11-25

## Context

The reorder decorator rebuilt each schema it decorated as a new model on
`BaseModel` alone, copying its fields, its configuration and its own
validator attributes. A project built from this style reported that a
decorated schema is no subclass of the classes its statement names when
the program runs, though the type checker treats it as one, so a guard
against one of those bases refused every decorated schema it was handed,
and the project's first run against a real database failed at such a
guard. Probing the decorator found the rest of what the rebuild drops.

## Evidence

Run on 2026-11-25 at 05a5f80. The template's decorated `User` ran as a
subclass of `BaseModel` alone, from the decorator's own module, and of
none of `IDMixin`, `UserBase` and `TimeStampMixin`. A decorated schema
lost its bases' methods, and neither its bases' validators nor its own
refused a value, though the decorator's docstring promised its
validators kept. Configuration built into the schema was lost as well,
since `User` declares `from_attributes`, yet validating it from an
object was refused unless the caller passed the flag, as the template's
translators do. Under Python 3.14, which defers annotations, the
decorator's own read of a class's annotations raised `NameError` for a
forward reference the class held, a reference the gate's lint asks to be
written unquoted. The template's decorated schemas carry no validator,
method, guard or forward reference, so nothing in its suites met any of
it.

## Options considered

- Registering the rebuilt model as a virtual subclass of each base.
  Refused, because the guard would pass while the methods and validators
  stayed lost.
- Building the new model on the original class's bases. Refused, because
  a model orders inherited fields first, so the order the decorator
  exists for could not be had.
- Writing in the decorator's docstring that a decorated schema is no
  subclass of its bases. Refused, because it documents a gap the type
  checker cannot see instead of closing it.

## Decision

The decorator reorders the class's own fields in place, rebuilds its
schema, and returns the class it was handed, so the schema keeps its
bases, methods, validators and configuration, and the order holds where
the model is written and described. A name the annotations carry that is
no field stays an attribute, a forward reference to a class not yet
defined resolves on first use as before, the annotations are read with
such a reference kept as a reference, and a class that is no pydantic
model is refused. The rebuild leans on the model's field mapping, which
pydantic keeps internal, so the cases hold it against an upgrade.

Nine cases join the decorator's suite and the ledger gains the claim.
Six breaks, each one point, each failed the suite. With the decorator as
it stood, the suite failed at import on the forward reference, and with
that reference quoted, seven of the new cases failed.

## Consequences

A guard against a decorated schema's base, a method a base gives it, and
a validator and a configuration it declares all hold as its class
statement reads. A pydantic upgrade that changes how a model holds its
fields fails the decorator's suite rather than a project's first run
against a database.
