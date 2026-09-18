# 0072. Refuse every connection that leaves the loopback in a suite

Status: Accepted
Date: 2026-09-18

## Context

The test contract placed suites, fixed substitution at the seams, forbade
patching a module's internals, and preferred a real adapter where one was
already suitable, because several of the shipped adapters are deterministic
and run in process. Nothing said a suite must be unable to reach a provider,
and nothing made it so. An adapter that reaches a commercial API resolves
its credentials the way its SDK does, from the environment, and the
library-citizenship rule forbids only reads at import time, so an adapter
constructed during a test on a machine with keys exported is a working
adapter, and it bills. An upstream entry of 2026-09-09 from a project at
pin e069bab89f81 reported exactly that, two command-line cases that had
always meant the deterministic stand-in scoring sixty samples against a
commercial model after a configuration document named a real one, noticed
only because a third assertion expected a refusal that no longer came.

## Evidence

Keel ships an adapter whose client falls back to the key in the environment
when none is passed, and its suite is safe today only because no test
constructs that adapter. ArchetypeCore's suite assigns fake settings before
any application module loads, so a real environment cannot leak into a run,
which is the principle stated for one seat's configuration and not for the
network. Helm's test setup already refuses every request no handler
answers, so the principle held there mechanically. On 2026-09-18 the three
Python suites were run under a plugin that refuses every connection leaving
the loopback, and all passed unchanged, while a probe that opened a
connection to an outside host was refused by name and the event loop's own
socket pair still worked. The harsher setting, refusing sockets outright,
broke asyncio's event loop on Windows, which builds itself a loopback pair.

## Options considered

- The reporting project's draft, a fixture clearing named credentials.
  Refused as the family's form, because it stops the authentication and not
  the request, its list of variables is the demo's stack and rots, and the
  entry itself says several SDKs fail only at the call, which is the request.
- Refusing sockets outright. Refused, because asyncio on Windows opens a
  loopback pair to wake its own loop, and the loopback is not the network.
- A sentence alone. Refused under the ladder, because the configuration can
  make the mistake fail before it bills, and a rule an agent has to remember
  is a rule that holds until the day it matters, as the entry said.
- Blocking in the adapters themselves. Refused, because product code has no
  business knowing it runs under a test, and a seam that checks for its
  test is the substitution the contract forbids in another coat.

## Decision

A suite cannot reach a provider or the network. In the Python seats
pytest-socket joins the development dependencies and the test configuration
carries the loopback restriction, so every connection that would leave
127.0.0.1 or ::1 is refused with the host named, and a test that must reach
a host declares it with the plugin's mark, in the open. In Helm the setup
that refuses every unhandled request is the same rule and is named as such
beside the line that does it. The test bullet of every guide states the
principle, the Test honesty gate item carries it, and the maps count it as
the sixth rule. Under the ladder the rule takes the check rung in the seat's
own configuration, which the style carries as law; making the reach
impossible would mean forbidding sockets, which the event loop needs.

## Consequences

An adapter constructed under a test with keys in the environment fails at
the connection with the host named, before anything is billed, and a test
that legitimately reaches a host says so where a reader sees it. The
reporting project drops its fixture at re-alignment and takes the
configuration. A subprocess a test spawns inherits the environment and not
the restriction, so a suite that spawns one is bound by the sentence there
and not by the plugin.
