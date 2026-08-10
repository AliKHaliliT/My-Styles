# 0013. Hold the type checker at strict

Status: Accepted
Date: 2026-08-10

## Context

Decision 0007 gave this template a type-check verb and was honest about its bar: the checker ran in default mode, because strict reported dozens of findings in hand-written code, and tightening was real work left to the owner. That left the two Python styles documenting the same verb while promising different things, since the package template holds strict with zero suppressions. The owner ruled that findings of ours get fixed conventionally, findings that are senseless to obey get a documented ignore, and anything in between gets surfaced.

The audit came back cleaner than the raw count suggested. Every finding was ours, and every one was a missing annotation rather than a type error: fifteen copies of one untyped ASGI callback across the middlewares, the field-reordering decorator's internals, two settings and auth sites where an untyped library call leaked `Any` into a declared return, the unit-of-work's untyped `__aexit__` on both the port and the implementation, and the composition root's three handlers. One nuance was not ours: `--strict` silently disables implicit re-exports, which would have declared war on the house convention that an `__init__.py` is a door.

## Options considered

- **Stay at default.** Rejected by the ruling: everything found was ours to fix.
- **Strict as-is.** Rejected: two hundred of the raw findings were the door convention being punished, not defects.
- **Strict with the doors kept implicit.** Accepted, which is also exactly the configuration the package template already runs.

## Decision

`strict = true` joins the mypy configuration with `implicit_reexport = true` retained, and all thirty-two genuine findings are fixed by annotation rather than suppression. The three pre-existing pins survive strict untouched, still marking Starlette's and pydantic's own annotation limits, still policed by `warn_unused_ignores`.

## Consequences

Both Python styles now promise the same thing when they say Type-check, and untyped code can no longer enter this template unnoticed. The cost was thirty-two annotations, most of them one mechanical pattern, and the standing rule that new code arrives fully annotated, which strict now enforces rather than requests.
