# 0120. Let a suite speak over Unix domain sockets

Status: Accepted
Date: 2026-10-22

## Context

The suite refuses every connection that would leave the loopback,
through the socket plugin's allowed hosts, so an adapter that reaches a
provider fails before it bills. Python 3.14 starts process workers
through a forkserver on Linux, and the forkserver talks to its workers
over a Unix domain socket, a connection with no host at all, which the
plugin refused as a connection to nowhere. A process-pool test in a
project built from the style failed inside the worker's setup before it
did any work, with no network in sight.

## Options considered

- Allow the socket in the one test that needs it, with the plugin's
  mark. Refused as the template's answer, because every process-pool
  test in every project would carry the same mark for a socket that
  names no host, and the rule is about hosts.
- Choose the spawn start method in the code under test. Refused, because
  a suite does not change production worker selection to pass, and the
  forkserver is the platform's default.

## Decision

The test configuration of the two Python seats and the arrow allows Unix
domain sockets beside the loopback, with the sentence that says why.
Such a socket names no host and never leaves the machine, and the
forkserver speaks through one. Every connection to a host outside the
loopback stays refused, and a test that must reach one still names it in
the open.

## Consequences

A process pool runs under the suite on every start method, and the
loopback rule keeps saying what it said about hosts.
