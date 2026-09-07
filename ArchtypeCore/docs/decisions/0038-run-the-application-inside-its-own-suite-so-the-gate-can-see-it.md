# 0038. Run the application inside its own suite so the gate can see it

Status: Accepted
Date: 2026-09-07

## Context

Two projects reported the same finding independently within a day. Three
uses of Starlette's deprecated 422 constant, a name Starlette now warns on
and will remove, sat in the validation handler and the shared response
documentation. The pytest configuration turns warnings into errors, per
record 0028, so a child whose suite imports the application fails at
collection. The template's own suite stayed green, because its one suite
imported domain interfaces and never the application, so the gate that
promised to catch a deprecation had no path to fire on. One of the two
reports also showed that the request-id middleware admitted websocket
scopes and then built a `Request` from the scope, whose constructor asserts
http, so every websocket connection died inside the middleware with a bare
assertion. The branch had been dead since the file's first commit, and its
docstring said the websocket path was implemented but not critically
tested, a debt sentence living in point-of-use documentation. A typo in the
request-id filter's error message rode along with the same report.

## Decision

The suite boots the application. `tests/test_main.py` builds the app
through Starlette's in-process test client and sends one malformed request,
so every module under `app` imports under the warnings gate and the
validation handler is seen answering in the standard error shape with the
request id echoed. The two observability middlewares are driven as the plain
ASGI callables they are, with an http scope and a websocket scope built by
hand, so the websocket branch is proven without a socket, and the two
not-critically-tested sentences leave their docstrings, because a test
replaces a caveat. The constant is renamed in its three places, the
middleware reads its headers off the scope, which both protocols carry, and
the typo is corrected.

The test client needs `httpx2`, added to the development requirements, and
its own import reaches anyio through a retired alias, so the configuration
gains its first named ignore, for that one message with the reason beside
it, which is the case record 0028 predicted would arrive from a dependency.

## Options considered

- The rename alone was refused, because it fixes the instance and leaves
  the gate blind to the next one.
- Proving the websocket branch through the test client was refused in
  favor of driving the ASGI callable directly, which needs no client and
  pins the exact contract that broke.
- Silencing the anyio warning by category or module was refused, because
  record 0028 allows a named ignore for one message and never a blanket.

## Consequences

CI executes the application it claims to test, and a deprecation in any
imported module is red on the day the dependency ships it. The middlewares'
websocket paths are proven rather than asserted in prose. The template's
first named warning ignore is on the record with its reason.
