# 0006. Document only directly thrown errors

Status: Accepted
Date: 2026-08-03

## Context

The family's doc-comment discipline requires fully documented functions to state their failure modes, and Keel settled the boundary question for Python: `Raises` lists only exceptions raised by the function's own body, because that is the only claim a reader can verify locally. Helm inherits the reasoning but not the syntax, since TSDoc's `@throws` is a repeatable tag rather than a prose section, and a sentinel entry like "Nothing." would render as a bogus item in every tooling surface that lists the tags.

## Options considered

- **Document every error that can escape the function.** Rejected: the escaping set is a property of the whole call tree, unverifiable locally and rotting as callees change; this is the same reasoning as Keel's record.
- **Mirror the Python sentinel with an explicit "@throws Nothing." on throw-free functions.** Rejected: tag-consuming tooling renders each `@throws` as a listed failure mode, so the sentinel reads as a documented error named "Nothing".
- **Direct-only `@throws`, with absence as the assertion.** Accepted.

## Decision

On a fully documented function, `@throws` carries one entry per error thrown directly by a `throw` statement in the function's own body, including defensive guards. An error that merely propagates from a callee is documented on the callee. The absence of `@throws` on a fully documented function is itself the assertion that the body throws nothing directly. `@returns` stays explicit on every fully documented function, writing `Nothing.` for void returns, because a return value is a single slot rather than a list and the sentinel reads naturally there.

## Consequences

Each error is documented exactly once, at the site that throws it, and any doc comment can be verified against its own function body. The cost is that absence now means something, so deleting a stale `@throws` is as much a documentation duty as adding one, and a reader tracing failure modes follows the call chain from the facade of the boundary, `shared/api`, where the two wire failures are documented in full.
