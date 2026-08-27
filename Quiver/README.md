# Quiver

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A strict, AI-ready host template for research-backed projects, keeping the question and its claims at the root while complete instances of the artifact styles produce the evidence as arrows under their own law.

Quiver is the family's host seat rather than a fourth peer. ArchetypeCore, Keel, and Helm answer how to build a thing; Quiver answers how to find out what to build and whether it works, and it carries the other styles inside it to do the building. It applies wherever a project should be run research-first, from an academic thesis to an industry feature whose worth is an open question, because the way a rigorous inquiry keeps its records does not change with the venue.

## The Philosophy: Why Does This Exist?

Software templates defend against entropy and attackers. An inquiry has a different adversary, self-deception, and it wins quietly: a result nobody can trace to the code that produced it, a dead end re-attempted a month later because its failure was never written down, a literature search that claims completeness over a region nobody bounded, a conclusion resting on an experiment the codebase has since outgrown.

Quiver's answer is one chain, kept short and mechanical. A question decomposes into conjectures. A conjecture becomes a claim only through evidence, and evidence names the exact commit of the arrow that produced it, so every truth the project holds is traceable to a reproducible state of the world. When an arrow moves past a pin, the claims resting on it are flagged, because knowledge that has silently stopped being backed is the most dangerous kind. Refuted conjectures are kept, not deleted, each with the evidence that killed it and the condition that would reopen it. The rest of the family's law, the two-tier checks, the immutable records, the prose rules, carries over unchanged, because honest record-keeping is the same discipline whether the subject is code or knowledge.

The rigor is proportional by law. The full spine is question, conjecture, evidence, claim, and any shortening is legal at the cost of one written line, so a feature-sized inquiry stays cheap and an omission stays a decision instead of an accident.

## The Domain Example: Why a Rounding-Drift Inquiry?

The demo asks a small, genuinely empirical question: when many monetary amounts are rounded to cents and summed, how much error does the tie-breaking rule accumulate? It is the right size for a template because the whole chain fits in view. The question lives in [docs/QUESTION.md](docs/QUESTION.md), one Keel-style arrow ([coinwise](arrows/coinwise/)) implements the strategies and the experiment, and the claim ledger holds the conjecture and what the evidence did to it, with every number pinned to the commit that produced it.

## Core Architectural Pillars

1. **The claim chain.** Question to conjecture to evidence to claim, with each claim's evidence quoted in full and pinned to the host commit whose tree produced it. A claim is the only place the inquiry holds a truth.
2. **Arrows under their own law.** Each embedded codebase is a complete instance of an artifact style, vendored whole under `arrows/`, governed by its own gate and conventions. Quiver's law binds the inquiry layer only, and a thin manifest per arrow is the whole interface.
3. **The graveyard.** A refuted conjecture is a result. It keeps its record, its killing evidence, its reopening condition, and its pin, which after cleanup is the only surviving proof the attempt existed.
4. **Staleness as a first-class state.** An arrow moving past a pin flips nothing by itself; it raises an advisory, and a person decides whether the claim is Stale, because only a person can tell whether the movement touched what the claim measured.
5. **Sources as objects.** Every consulted work is a self-contained citation with its edition named, addressed by key, so no source vanishes by being treated as the frame instead of the thing.

## Project Structure

```text
Quiver/
  AGENTS.md              The operating manual, the gate, and the documentation index.
  STATE.md               What is in flight, queued, deferred, or blocked.
  docs/
    QUESTION.md          The root question and its open conjectures.
    ARCHITECTURE.md      The map of the inquiry.
    BIBLIOGRAPHY.md      Every consulted work, cited by key.
    CONVENTIONS.md       The frozen documentation rulebook.
    BASELINE.md          The repository baseline.
    decisions/           Immutable decision records.
    claims/              Immutable claim records, the inquiry's knowledge.
    arrows/              One living manifest per arrow.
  arrows/
    coinwise/            A Keel-style library arrow, whole and under Keel's law.
  scripts/
    audit_inquiry.py     The mechanical half of the rules, with a selftest.
```

## Key Features

- **Traceable knowledge**: every claim's evidence pins the commit that produced it, checked mechanically against git history.
- **Two-tier checking from birth**: shape rules gate, the stale-pin scan advises, and every advisory must be answered in writing.
- **A dead end cannot be re-attempted unknowingly**: refuted conjectures stay in the ledger with reopening conditions.
- **Proportional rigor**: the spine is complete, and every legal shortening costs exactly one recorded line.
- **Host-kind by construction**: any artifact style loads as an arrow, and future arrows need not be code.

## Getting Started

```bash
# Audit the inquiry layer (documents, claims, citations, pins).
python scripts/audit_inquiry.py

# Prove the audit's own rules against planted defects.
python scripts/audit_inquiry.py --selftest

# Work the demo arrow under its own law.
cd arrows/coinwise
pip install -e . && pip install --group dev
pytest && ruff check . && lint-imports && mypy src tests
```

## Conventions

Documentation follows the family's two-species system, extended for inquiry: living documents describe the present and records describe one past event, with claims joining decisions as a second record kind whose Evidence sections quote results in full and pin the commits that produced them. The full rulebook, including the claim template, the pin and staleness rules, the bibliography rules, and proportional rigor, lives in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); that file is normative and must not be modified. The rationale behind the system is recorded in [its founding decision record](docs/decisions/0001-adopt-the-documentation-system-and-extend-it-for-inquiry.md). Code carries no house docstring rules at this level, because code lives in arrows and each arrow's style governs its own.

Both the rulebook and the conventions above are owned at the style level. A project built from this template never changes them locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

One further rule applies to every piece of prose in the project, from this README through claim records to commit messages. Everything must read as if a person wrote it. The clearest machine tell is the clause-colon splice, a sentence shaped as claim, colon, elaboration; no human writes that way outside a slide deck, so in prose a colon may only introduce a list, a quote, or a label. Softer tells, such as a balanced semicolon antithesis or a neat triadic list, are each fine on their own but give the text away when stacked, because a paragraph of polished epigrams reads as machine writing even when every sentence would pass alone. Allow at most one such flourish per paragraph and write the rest as plain declarative sentences.

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
