# coinwise

A small library measuring the drift that a rounding strategy accumulates when
many monetary amounts are rounded to cents and summed. It exists to produce the
evidence behind the claims of the Quiver inquiry that hosts it, and it follows
the [Keel](../../../Keel/) style: src layout, bare-namespace layer portions with
re-exporting leaf packages, the NumPy docstring convention with the house
`Usage` block, seam-only test substitution, and the Dependency Rule enforced by
import-linter.

Like every demo in this family, it is deliberately incomplete in named ways. As
an arrow it carries only what the inquiry needs, so there is no documentation
spine, no CI of its own, no command-line entry point, no packaging metadata
beyond what the tooling reads, and no baseline dotfiles, since the host's
copies at the Quiver root govern this tree. This README is a working note
rather than an instance of Keel's README schema. The gaps above are permanent,
and the list was drawn by reading Keel's baseline and README schema against
this tree file by file.

## Commands

- Install (editable): `pip install -e .` (Python 3.14+; add the tooling with `pip install --group dev`)
- Test: `pytest`
- Lint: `ruff check . && lint-imports`
- Type-check: `mypy src tests`

## Layout

```text
src/coinwise/
  domain/rounding/          The two strategies and the tie test they disagree on.
  services/accumulation/    Summing a stream twice and measuring the drift.
  facade/experiment/        The deterministic grid and the one-call experiment.
tests/                      Mirrors the source tree, one suite per unit.
```
