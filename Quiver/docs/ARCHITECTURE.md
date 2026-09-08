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
them. Movement of an arrow past a pin, or past a claim's latest verification,
raises the audit's advisory, and a person answers it by re-verifying in the
arrow's manifest when the figures reproduce, superseding when they do not, or
flipping to Stale. A recorded observation is never advised, because no command
could have changed it.

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

## Passes over the literature

Reading enters the same chain as running. A pass over one slice of the question is bounded before it begins and leaves one dated record in `docs/reviews/`, naming what it searched, the stages it ran or collapsed, the keys it found, and the ledger entries it moved; the bibliography, the claims, and the decomposition hold what it found, so no synthesis document sits beside them to rot. The next pass over the slice extends the last from the date it stopped.

## Exemplars

The map says where things live; these files say how they read. An artifact of a kind listed here is cut from its exemplar and rewritten, never written fresh from the rule, because the rule names what must exist and only these bytes carry the dialect. The demo's named incompleteness bounds what the exemplars cover, not how closely they are followed.

- A settled claim with its pin and figures: `docs/claims/0009-half-even-cancels-the-drift-that-half-up-accumulates.md`.
- A superseded claim, showing the re-pin form: `docs/claims/0007-half-even-cancels-the-drift-that-half-up-accumulates.md`.
- A decision record: `docs/decisions/0009-advise-only-on-movement-that-can-move-a-number.md`.
- An arrow manifest: `docs/arrows/coinwise.md`.
- The question with its decomposition: `docs/QUESTION.md`.
- A review pass record: `docs/reviews/2026-09-05-tie-breaking-in-monetary-rounding.md`.
