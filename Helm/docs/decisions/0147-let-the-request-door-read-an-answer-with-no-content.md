# 0147. Let the request door read an answer with no content

Status: Accepted
Date: 2026-11-26

## Context

The request door reads every answer the backend gives. A refusal it
turns into one typed error and a payload that breaks the wire contract
into another, so a caller meets typed data or a typed failure. It read a
success by handing the body to the JSON reader before the schema saw
anything, and a project built from this style reported that an answer
with no body, the 204 a server commonly sends once a removal is done,
therefore rejected with the JSON reader's own error. The door sends a
DELETE, the method whose usual answer it could not read, and the project
had shaped its server's routes around the gap.

## Evidence

Run on 2026-11-26 at 964c295, in a suite of the probe's own against the
pretend backend. A 204 with no body rejected with a `SyntaxError` saying
the JSON input had ended, whatever schema the caller passed, a 200 with
no body did the same, and a 200 whose body was a page of markup rejected
with the reader's complaint about its first character. None was either
of the door's errors, and the rule for asking a failed query again took
each for a failure that carried no answer, to be asked three more times.
No code of the template sends a DELETE, the pretend backend answers
none, and no case of the door's suite met a success without JSON.

## Options considered

- Reading only a 204 or a 205 as nothing. Refused, because a server may
  answer a removal with a 200 and no body, and a success that is not
  JSON would still escape as the reader's error.
- A second door, or an option, for a request that expects no content.
  Refused, because the schema already says what a caller expects, and a
  schema of nothing says it without a second way in.
- Answering every empty body with nothing, whatever the schema. Refused,
  because an endpoint that promised content and sent none has broken its
  contract, and the caller should hear so.

## Decision

The door reads a success as text. An empty body is nothing and anything
else is parsed as JSON, and the value, nothing included, is checked
against the caller's schema, so a schema of nothing accepts an answer
with no content and a schema that expects content refuses it as a broken
contract. A body that is not JSON is refused as a broken contract too,
with the path and that reason. The map's steps and the ledger say so.
Four cases join the door's suite, and nine breaks, each one point, each
failed a case.

## Consequences

A caller that removes a resource passes a schema of nothing and reads
the server's plain answer through the door. A success the door cannot
read reaches its caller as a broken contract, which the retry rule never
asks again. The reporting project can answer its removals plainly at its
next re-alignment.
