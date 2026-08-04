# 0002. Adopt the repository baseline

Status: Accepted
Date: 2026-08-03

## Context

The family's repository baseline also predates Helm. It exists because always-present files used to accumulate by inheritance rather than by decision, line endings depended on per-machine git configuration, and one derived deployment showed that the documentation system's own faithfulness can leak sensitive context into tracked files. Helm adopts the baseline at birth, so the question was what the Node-stack instantiation of it looks like.

## Options considered

- **Inherit a stock Node .gitignore.** Rejected: stock files carry rules for tools this project does not use, and every rule present must be a decision rather than an inheritance.
- **Track the generated msw worker script, as msw's docs suggest.** Rejected: the file is regenerated on every install through the manifest's `workerDirectory` setting, and the baseline already classifies regenerable artifacts as never tracked.
- **A curated baseline instantiated for this stack, with the private-ledger rule included from birth.** Accepted.

## Decision

Adopt the repository baseline specified in [BASELINE.md](../BASELINE.md): an always-present set (`README.md`, the manifest and its committed lockfile, `.gitignore`, `.gitattributes`, `.editorconfig`, plus the documentation spine), a conditional set with explicit triggers (`LICENSE`, `.env.example`, `CHANGELOG.md`, `util_resources/`), a never-tracked set (editor directories, secrets, regenerable artifacts including `node_modules/`, `dist/`, and the msw worker, OS junk), and the public-audience rule with `LOCAL.md` as its outlet: every tracked byte and every commit message is written for a public audience regardless of current visibility, and sensitive context goes to the untracked local ledger instead.

## Consequences

Clones behave identically regardless of the contributor's editor, operating system, or git configuration; the ignore file reads as a description of this stack rather than an inventory of all stacks; and the sensitive-context rule holds from the first commit instead of being retrofitted. The cost is that the lockfile must exist and stay committed, which requires an install on a machine with Node before the template is complete, and that shared editor behavior must be expressed through `.editorconfig` or tool configuration rather than a tracked `.vscode/`.
