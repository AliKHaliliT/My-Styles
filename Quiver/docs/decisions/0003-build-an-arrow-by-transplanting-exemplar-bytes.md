# 0003. Build an arrow by transplanting exemplar bytes

Status: Accepted
Date: 2026-08-27

## Context

The first arrow was reviewed against the style it claims, and it had drifted.
Not in structure, and not in anything a gate checks. The src layout, the
portions, the mirrored tests, and the five commands were all faithful, and
every check ran green. The drift was in the dialect, the layer of a style that
no rulebook sentence carries, and it was systematic rather than occasional,
because the arrow had been written from the rulebook's summary of Keel instead
of from Keel's own files.

The failure mode generalizes. A style's conventions name what must exist,
sections, sentinels, seams, and a writer who knows only the summary produces
code that satisfies every named rule in a foreign voice. Inside a style's own
repository the trap barely exists, since new code is written surrounded by
exemplars and matches them naturally. An arrow is the exposed case, a fresh
tree built beside its style rather than inside it, where the summary is the
only thing a writer holds unless the law sends them to the bytes.

## Evidence

The review that surfaced the drift, run against the trees at commit 93c2325.
Keel's thirty non-init src modules carry zero module docstrings, while the
arrow put one on every module and every re-exporting door. Keel spreads every
docstring, a blank line after the signature, the quotes alone, two blank lines
between sections, while the arrow's were uniformly tight. Keel's eight
validation guards all speak one sentence shape, "x must y. Received: {value}
with type {type}", while the arrow's one guard said "count must be at least 1".
Keel's Usage blocks are fenced code, the arrow's were doctest lines. Every gate
passed on both sides throughout, which is correct, because each of these lives
in the judgment tier where no check may decide.

## Decision

An arrow is begun by transplanting the nearest exemplar files from its style
and rewriting their words, never by writing fresh from a rule summary. Review
of a new arrow reads it beside the exemplars it was cut from, not beside the
rulebook.

The rule lives in the rulebook's arrows section, and it is judgment tier. No
check compares dialect, because rhythm and voice are exactly what a mechanical
rule cannot decide without freezing accidents into law, and a checker for
"reads like the style" would gate on its own taste.

## Consequences

Building an arrow starts with a copy instead of a blank file, which costs
nothing and removes the entire class of summary-shaped drift, since whatever
the writer never thought about arrives correct by inheritance. The rulebook
stays a summary and stops being mistaken for the style itself.

The first arrow was rewritten into Keel's dialect under this rule, which moved
it past the pins of the claims resting on it. That is the staleness advisory's
question to raise, as designed, and the owner answers it per the claim rules.
