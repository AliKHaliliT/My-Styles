# 0005. An arrow is a full adaptation of its style

Status: Accepted
Date: 2026-08-27

## Context

Record 0003 fixed how an arrow is begun, by transplanting exemplar bytes, and
left open how much of the style the finished arrow keeps. The first arrow kept
the code, the tooling, and the tests, and named the rest away as incompleteness,
no documentation spine, no dotfiles, no workflow. That trim was survivable only
in the showcase repository, where the style sits next door. In an instantiated
inquiry the style is not present at all, so an agent working inside such an
arrow would have no AGENTS.md to read, no conventions to follow, and no
decisions folder to record a choice in, and the owner's question that prompted
this record put it plainly, the arrow must be able to decide for its own code.

The multi-style worry dissolves under the same mechanics. AGENTS.md,
`.gitignore`, `.gitattributes`, and `.editorconfig` all scope to their subtree
with nearest-file-wins semantics, so a Keel arrow and a Helm arrow each carry
their own law and nothing ever has to merge or rank the styles at the host
level, which the host's own rulebook already forbids by keeping code law out of
the inquiry layer.

## Decision

An arrow is a full adaptation of its style. It carries the style's entire
documentation spine, AGENTS.md, STATE.md, the docs folder with the frozen
rulebook, the baseline, the architecture map, and the inherited decision
records, plus the docs audit script, the baseline dotfiles, and the style's
inert workflow. Named incompleteness in an arrow's README covers domain trims
only, a demo that needs no CLI may say so, and never the spine.

The LICENSE file alone stays at the host root, since a license answers a
repository-level question and an arrow is a subtree of one work. An arrow
extracted to stand alone gains its own license then, following its style's
baseline trigger, and its carried inert workflow activates the same day, which
is what makes extraction a rename rather than a reconstruction.

The demo arrow was brought up to this shape rather than grandfathered, because
the first arrow is the exemplar future arrows are cut from and it teaches
whatever shape it has. Bringing it up also surfaced one code debt the trimmed
form had hidden, a services object crossing the public surface, now flattened
through a facade translator per the style's own boundary ruling.

## Options considered

- Style digests in the host's guide, a summary of each style's coding rules
  beside the inquiry law, were refused. A digest is the rule-summary failure
  mode institutionalized, it drifts from the style it summarizes, and record
  0003 exists because summaries are exactly what agents must not build from.
- Per-arrow LICENSE files were refused while the arrow lives in a host, since
  duplicating the owner's own license per subtree states nothing new and the
  baseline's trigger rule already covers the extraction case.
- Leaving the demo arrow trimmed, with its gaps named, was refused because an
  exemplar with named gaps still teaches the gaps.

## Consequences

The host CI now runs the arrow's docs audit and seam check beside its lint,
type, and test steps, so the full gate of every arrow is exercised where the
host's history lives, and the inert copy inside the arrow waits for
extraction. An agent standing anywhere in the tree finds the binding law by
proximity, the inquiry's at the root, the arrow's inside the arrow.

Arrows get heavier by roughly a spine's worth of files, which is the honest
price of the word whole in "vendored whole", and the trimmed alternative
already produced one dialect drift and one hidden boundary leak, so the weight
buys the thing the seat exists for.
