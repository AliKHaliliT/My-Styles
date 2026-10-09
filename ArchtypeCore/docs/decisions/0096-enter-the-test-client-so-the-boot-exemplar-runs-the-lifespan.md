# 0096. Enter the test client so the boot exemplar runs the lifespan

Status: Accepted
Date: 2026-10-09

## Context

The boot suite exists to boot the whole application in process and
send one malformed request, so every module imports under the warnings
gate and the validation handler is seen answering in the standard
shape. It constructed the test client and never entered it, and
Starlette runs an application's lifespan only inside the client's
context, so the startup and shutdown this seat defines, the logging
configuration today, never ran under the suite. A dependency a project
initialises at startup fails under such a boot before the body is
validated. A project built from this style, which initialises its
request dependency in the lifespan, reported it on 2026-10-08 after
the derived boot case failed and passed once the client was entered;
the template's own demo passed because nothing it needs is made at
startup.

## Evidence

Measured on 2026-10-09. `tests/test_main.py` constructed the client
outside any context and `main.py` passes a lifespan that configures
logging, so the suite's boot skipped the one piece of startup the seat
has. With the client entered, the suite passes unchanged in its
assertions and the lifespan runs before the request and after it.

## Options considered

- Leaving the exemplar as it was and noting the context form in the
  rulebook. Refused, because the exemplar is what a project cuts its
  boot case from, and a sentence beside a wrong exemplar loses to the
  bytes.
- A fixture yielding an entered client for every suite. Refused for
  now, because the boot case is the one suite that speaks to the whole
  application, and the middleware suites drive their callables without
  a client by design.

## Decision

The boot exemplar enters the client around its one request, written
as `with TestClient(app) as client`, so the application's startup
runs before the request and its shutdown after it, as in a deployment,
and the map says the boot enters the lifespan.

## Consequences

A project's boot case, cut from the exemplar, exercises what its
lifespan makes, and a dependency initialised at startup is proven by
the same request that proves the validation shape.
