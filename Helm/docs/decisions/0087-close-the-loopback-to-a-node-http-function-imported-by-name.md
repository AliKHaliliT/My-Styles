# 0087. Close the loopback to a Node HTTP function imported by name

Status: Accepted
Date: 2026-09-30

## Context

The test setup started the mock server in a hook and refused every
request no handler answered, and the guide said no request leaves the
loopback. A project built from this template reported on 2026-09-18 that
a suite importing a function by name from the Node HTTPS module reached
real name resolution while the server was listening. The interceptor
patches the module object, which a default import and fetch go through,
but Node keeps a separate namespace for the module's named exports and
updates it only when asked, and a test file binds a named import as it
loads, before any hook runs.

## Evidence

Reproduced on 2026-09-30 with the template's setup, on Node 24, Vitest 4
and MSW 2.15. A request through a function imported by name from the
Node HTTPS module reached name resolution and failed with the host not
found, while the same request through the default import and through
fetch was refused with the server's own message. Synchronizing the
built-in module's exports inside a hook changed nothing, because the test
file had already bound the original. Starting the server and synchronizing
as the setup file loads, before the test file's imports, refused the named
caller with the same message, through the request's own error event, with
no pending caller and no unhandled rejection.

## Options considered

- A catch-all handler answering every unmatched request with a network
  error, which the reporting project added beside the refusal. Refused,
  because with these versions the refusal already reaches the caller's
  error event, and the handler would turn a loud refusal that names the
  strategy into a silent failure a test could swallow.
- Forbidding named imports from the Node HTTP modules by lint. Refused,
  since the hole was in how far the interception reached, not in a
  spelling, and closing the reach covers every spelling, in scripts as in
  suites.
- Starting the server and synchronizing the built-in exports as the
  setup loads, and synchronizing again after it closes. Adopted.

## Decision

The test setup starts the mock server as it loads rather than in a hook
and synchronizes Node's built-in module exports right after, and after
the server closes it synchronizes them again so the originals return. A
suite for the mock server proves both entrances, a fetch and a request
through a function imported by name from the Node HTTPS module, each
refused with the server's message; the named entrance failed with the
host not found before this change and passes after it. The suite takes
the raw fetch entrance under a per-file waiver in the lint configuration
with its reason beside it, the form record 0024 prescribes, since the
rule that sends product code through the request helper stands on this
very refusal. The invariants ledger gains the row, and the guide's test
bullet and the map's testing paragraph name both entrances.

## Consequences

A suite cannot reach a host through any import form of the Node HTTP
modules while the setup runs, and a reader of the ledger sees the claim
held by a listed case rather than by a sentence. A project that reported
the hole takes the setup's form and drops its catch-all handler, or keeps
it as its own decision.
