# Architecture

The map of the inquiry as it is today. The inquiry layer holds no code beyond
the audit script; its structure is the flow of knowledge.

## The flow

```text
docs/QUESTION.md ──decomposes into──▶ conjectures (claims at Status: Conjecture)
        │                                     │
        │ cites                               │ runs an experiment in
        ▼                                     ▼
docs/BIBLIOGRAPHY.md                 arrows/<name>/   (that style's law)
                                              │
                                              │ produces results, quoted and
                                              │ pinned to the host commit
                                              ▼
                             docs/claims/NNNN  (Conjecture, Supported, Refuted, Stale, Superseded)
                                              ▲
                       docs/arrows/<name>.md  lists what rests on each arrow
```

A conjecture is written before its experiment. Evidence flips it to Supported
or Refuted, quoting the results and pinning the commit whose tree produced
them. Movement of an arrow past a pin raises the audit's advisory, and a
person answers it by re-running at a new pin, superseding, or flipping to
Stale.

## The arrows

One arrow today. [coinwise](arrows/coinwise.md) is a Keel-style library
carrying the rounding strategies, the accumulation service, and the
one-call experiment facade. Its layers obey Keel's Dependency Rule, enforced
by its own import-linter configuration.

## Testing

The inquiry layer is tested by `scripts/audit_inquiry.py`, whose own rules are
proven by `--selftest` against planted defects. Arrow code is tested by each
arrow's own suite under its own style's testing contract; the audit never
reaches into an arrow, and an arrow's suite never checks a claim.
