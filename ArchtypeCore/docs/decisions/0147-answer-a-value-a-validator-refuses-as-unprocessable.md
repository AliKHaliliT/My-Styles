# 0147. Answer a value a validator refuses as unprocessable

Status: Accepted
Date: 2026-11-25

## Context

The validation handler sent the errors a request's validation produced
as they stood. A project built from this style reported that a request
schema whose field validator refuses a value by raising `ValueError`
leaves the exception itself in the error's context, so the response
cannot be encoded, building it raises a `TypeError`, and the general
handler answers the request with a 500 instead of a 422.

## Evidence

Run on 2026-11-25 at 05a5f80 with the seat's development requirements. A
model whose validator refuses a blank name left an error whose context
held the `ValueError`, and the handler, called with it, raised
`TypeError: Object of type ValueError is not JSON serializable`.
FastAPI's own encoder writes the exception as an empty object. No
request schema of the template has a validator that raises, and the boot
suite's malformed request lacks a field, whose error carries no
exception, so no case reached the path.

## Options considered

- Encoding the errors by FastAPI's own rule. Refused, because it answers
  the request but writes the exception as an empty object, so the 422
  loses the validator's reason.
- Asking each schema to refuse with an error of its own instead of
  raising. Refused, because the handler is the one place every refusal
  passes, and a rule each schema must remember is one a schema forgets.

## Decision

The handler encodes the errors with each exception in a context written
as its message, so a value a validator refuses is answered 422 in the
standard shape with the validator's reason. A case builds the errors
from a model of its own whose validator raises, calls the handler as a
plain function, and reads the status, the shape and the reason, and the
ledger gains the claim. Two breaks, each one point, the raw errors sent
again and the exceptions encoded by FastAPI's own rule, each failed the
case.

## Consequences

A project that adds a validator to a request schema gets a 422 that
carries the validator's reason, where it got a 500.
