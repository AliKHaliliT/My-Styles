# 0089. Say what a pydantic model's docstring becomes in a schema

Status: Accepted
Date: 2026-10-05

## Context

The lint selection requires a docstring on every public class, and
pydantic copies a model's class docstring into the JSON schema it
generates as the schema's description. A project built from the host
style with an arrow of the package style reported on 2026-10-04 that a
verdict model its code asks a language model to fill, given a docstring
to meet the lint, changed the tool description the model received, with
words written for a reader of the source. It dropped the docstring from
the schema through the model's schema hook and asked whether the
template wanted an exemption from the docstring rule, a convention for
schemas a model reads, or the suppression as the form.

## Evidence

Measured on 2026-10-05 on this template's own models under pydantic
2.13. The generated schema of a model carries its docstring as the
description, and a schema hook that removes the key leaves the rest of
the schema whole. This template sends a model's
schema to no language model. Its schemas reach the API documentation,
where the docstring is the description a reader of the API expects, so
the sentence binds only what a project adds.

## Options considered

- An exemption from the docstring rule for models a language model
  fills. Refused, because the reader of the source is the one the rule
  serves and would lose the docstring for a reason that is the schema's.
- The suppression as the only form. Refused, since the translator that
  builds what a provider sees is the house's answer to a wire shape, and
  the hook is the second form, for a model handed over whole.
- Saying nothing, as the template's own bytes never trip it. Refused,
  because the library copies the docstring without being asked and a
  project found out by what its model was told.

## Decision

The docstring convention says that a pydantic model's docstring is also
the description of the schema generated from it, so a schema a language
model reads is built by a translator from fields named for it, or the
model drops its docstring from the schema with the reason beside it, and
the docstring stays written for the reader of the source. The
sentence stands in the rulebook's section on code-level documentation,
with the API documentation named as the schema that keeps the docstring.

## Consequences

A project that hands a model's schema to a provider decides what the
provider reads, in the translator or in the hook, and a reviewer finds
the sentence that asks it to. The docstring rule stands unchanged.
