# 0116. Keep the lint stack current and override its matcher

Status: Accepted
Date: 2026-11-02

## Context

The lint stack stood at ESLint 9 with the plugins of that year, and the
package manager's audit at the pin named twenty-two findings, six of
them high, in the development tree. One was a path matcher below 11.0.1
under ESLint's own dependencies, which no update inside the declared
ranges reaches because the patched matcher is a new major with different
exports; the rest were in-range findings in the build tool, the schema
library and their helpers. A project built from this style met the
matcher first, in a dependency audit of its own, and upgraded its lint
stack to ESLint 10 with an override on the matcher.

## Options considered

- A global override alone, on ESLint 9. Refused, because ESLint 9 calls
  the old matcher's interface and the patched major does not offer it,
  so the lint command would break against its own dependency.
- Leave the development tree as it stands, since nothing in it ships.
  Refused, because the gate runs the tree on every push and a matcher
  that can be made to spin is a gate that can be made to hang.

## Decision

The lint stack moves to ESLint 10 with the plugins that declare it, the
matcher is overridden to 11.0.1 or later while ESLint's own tree still
asks for the older major, and the dependencies inside their declared
ranges take their current patches, all measured together. The audit
reports nothing, lint, types, tests and build pass, and the core quote
rule the style enforces still fires under ESLint 10, so the move to the
stylistic plugin that record 0015 anticipated is not due yet. The
override is temporary and leaves with the first ESLint tree that asks
for the patched matcher itself.

## Consequences

The development tree audits clean today, the lint gate keeps the rules
it had, and a project that copies the manifest inherits the override
with its condition to drop it.
