# 0129. Replace the token library and bind the algorithm to the secret

Status: Accepted
Date: 2026-11-03

## Context

The dependency audit's first run named two advisories in this seat's
set, neither with a fix release. One was in the token library, whose
guard against an asymmetric key handed to HMAC verification can be
bypassed with a DER-encoded key, and whose last release predates the
advisory by more than a year; the other was a timing attack in the
signing library it carries for ECDSA, which that library's maintainer
leaves out of scope. The seat reached neither, since it signs and
verifies with one shared secret under the one algorithm its settings
name, and both were dismissed in writing. A dismissal the gate repeats
at every push for a library that leaves its advisory unfixed is debt the
tree carries, and nothing in the configuration said that the adapter's
shape admits only an HMAC algorithm. The replacement library also warns
when a secret is shorter than the hash output of the algorithm it
serves, and the seat's floor of thirty-two characters fit HS256 alone.

## Options considered

- Keep the library and dismiss the two findings at every gate. Refused,
  because the dismissal rested on the seat's shape and not on the
  library, and a library whose maintainer leaves a published advisory
  unfixed is the wrong one to rest on.
- Take a larger library that covers the whole signing and encryption
  family and the authorization flows around it. Refused, because the
  seat signs and verifies one kind of token with one secret, and the
  breadth would be weight with nothing to carry.
- Sign and verify by hand with the standard library's HMAC. Refused,
  because the expiry, the required claims and the refusal of an unsigned
  or differently signed token are what a token library is for, and a
  hand-written one would own every mistake a maintained one has already
  made and fixed.

## Decision

PyJWT replaces python-jose. It is maintained, pure Python with no
runtime dependency on this interpreter, and audits clean, so the seat's
set carries no advisory. The adapter encodes as before and decodes under
the configured algorithm alone, requiring the expiry and the subject,
and maps every library error to the refusal it already returned. The
settings refuse an algorithm outside the HMAC family with the reason,
because the local adapter signs and verifies with one shared secret and
an asymmetric algorithm needs an adapter with two keys, and they require
the secret to be at least as long as the configured algorithm's hash
output, thirty-two, forty-eight and sixty-four bytes, as RFC 7518
requires and the library warns below; the environment example says both.
The mypy override the old library needed goes. A suite covers the
adapter, the round trip, an expired token, one signed with another
secret, one signed under another algorithm, one unsigned, one without an
expiry or a subject, a string that is no token, the type guards and the
password hash, the settings suite covers the two validators, and the
ledger gains the five rows they hold.

## Consequences

The dependency audit of this seat prints nothing, the runtime image
loses the cryptography, RSA, ECDSA and ASN.1 libraries the old token
library carried, and a project that wants asymmetric signing writes an
adapter with two keys and lifts the validator with a record of its own.
