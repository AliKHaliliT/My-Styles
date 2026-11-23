# 0132. Ask a query again only when no answer came

Status: Accepted
Date: 2026-11-23

## Context

The app's query client set no retry option, so the library's default
applied, and a query the backend refused was asked three more times,
with a growing wait between, before its error reached the page. The
cache calls its error hook only after the last retry, so the sign-out on
a 401 waited as well. The suites never met it, because the test client
turns retries off. A project built from the client style timed it in a
browser against its server, and sent the case as an entry.

## Evidence

Measured in the style's own suite, with the vessel page rendered under
the app's own client for an id that is not on the books. At afffa40, on
2026-11-22, the reason showed after 8,328 ms, and the vessel was asked
for four times. With the change, on 2026-11-23, it showed after 357 ms,
asked for once. The entry measured 7,467 ms and four requests against
114 ms and one in its own client.

## Options considered

- Turning retries off for every query. Refused, because a lost
  connection or a server that failed for a moment is worth asking again,
  and the cache's growing wait is the right tool for it.
- Never retrying any refusal the client raises, a server's own error
  among them, as the entry proposed. Refused, because a 5xx may pass,
  and is asked again as before. Only a refusal under 500 is an answer.
- Asking again after a 408 or a 429, which tell a client to come back
  later. Left out, because neither the style's server nor its mock sends
  one. It reopens when a backend a project talks to does.

## Decision

A rule in the shared API segment decides whether a failed query is asked
again. A refusal under 500 and a payload that broke the contract are
answers and are never retried, and any other failure is asked again
three times, the cache's default. The app's query client takes the rule
for every query, and a mutation keeps the cache's default of no retry.
Cases hold each refusal, the broken contract, a server's error and a
failure that carried no answer up to the last retry, and the app's own
client asking a refused query once. Seven breaks of the rule were each
caught. The ledger gains the claim, and the map says what is retried and
why.

## Consequences

A refusal reaches its page on the first reply, and a 401 signs the
session out at once. A backend that answers a passing fault with a 4xx
is not asked again, and its page shows the reason it gave.
