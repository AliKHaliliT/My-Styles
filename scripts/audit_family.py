"""Audit the family's shared law for drift between the styles.

The styles replicate certain blocks of law by hand: the delivery gate in the
three artifact guides (the host's gate is its own by design), the upstream
report in every guide, the rulebook's shared core, and the docs audit the two
Python styles carry as one script. Replication without drift detection is the
failure mode this family refuses to tolerate in its derived projects, so the
same standard applies here. The manifest below is also the blueprint. When a
new style joins the family, the blocks that fit its kind are what it must
carry, and adding it to the file lists is what puts it under guard.

The second duty is the carried copies. An arrow living in this repository is
a full adaptation of its style and carries pieces of that style verbatim, so
while the two share this roof the copy tracks the original, and this script
is what holds it there. The gate lives at the host root on purpose, because
no arrow carries this script and no extraction copies it. An instance created
out of this repository freezes at extraction, owes its style nothing
afterward, and holds no bytes that depend on a tracking mechanism. Adapting
to later revisions of the style is the child owner's own refactoring choice.

Anchors cut a block from its file: text from the start anchor (inclusive) to
the end anchor (exclusive), or the whole file when both anchors are None. A
block passes when every copy is byte-identical.
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCKS = [
    (
        "the delivery gate",
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md"],
        "## The delivery gate",
        "## The upstream report",
    ),
    (
        "the upstream report",
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md", "Quiver/AGENTS.md"],
        "## The upstream report",
        "## Adopting this style",
    ),
    (
        "the adoption section",
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md", "Quiver/AGENTS.md"],
        "## Adopting this style",
        "## Documentation index",
    ),
    (
        "the rulebook's shared core",
        [
            "ArchtypeCore/docs/CONVENTIONS.md",
            "Keel/docs/CONVENTIONS.md",
            "Helm/docs/CONVENTIONS.md",
        ],
        None,
        "## Code-level documentation",
    ),
    (
        "the docs audit",
        ["ArchtypeCore/scripts/audit_docs.py", "Keel/scripts/audit_docs.py"],
        None,
        None,
    ),
    (
        "the prose law",
        [
            "ArchtypeCore/docs/CONVENTIONS.md",
            "Keel/docs/CONVENTIONS.md",
            "Helm/docs/CONVENTIONS.md",
            "Quiver/docs/CONVENTIONS.md",
        ],
        "## Prose",
        None,
    ),
    (
        "the em dash rule",
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md", "Quiver/AGENTS.md"],
        "- An em dash is legal",
        "- Commit history speaks",
    ),
    (
        "the prose hard rule",
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md", "Quiver/AGENTS.md"],
        "- All prose must read",
        "- Every tracked byte is public prose",
    ),
]

# What each arrow carries verbatim from its style: (name, original, copy, start
# anchor or None for the whole file). The original is canonical; a divergence
# is fixed by rewriting the copy, never the original.
CARRIES = [
    (
        "agent guide shared tail",
        "Keel/AGENTS.md",
        "Quiver/arrows/coinwise/AGENTS.md",
        "The checks report at two levels",
    ),
    (
        "rulebook",
        "Keel/docs/CONVENTIONS.md",
        "Quiver/arrows/coinwise/docs/CONVENTIONS.md",
        None,
    ),
    (
        "baseline",
        "Keel/docs/BASELINE.md",
        "Quiver/arrows/coinwise/docs/BASELINE.md",
        None,
    ),
    (
        "docs audit",
        "Keel/scripts/audit_docs.py",
        "Quiver/arrows/coinwise/scripts/audit_docs.py",
        None,
    ),
    (
        ".gitignore",
        "Keel/.gitignore",
        "Quiver/arrows/coinwise/.gitignore",
        None,
    ),
    (
        ".gitattributes",
        "Keel/.gitattributes",
        "Quiver/arrows/coinwise/.gitattributes",
        None,
    ),
    (
        ".editorconfig",
        "Keel/.editorconfig",
        "Quiver/arrows/coinwise/.editorconfig",
        None,
    ),
    (
        "inert workflow",
        "Keel/.github/workflows/ci.yml",
        "Quiver/arrows/coinwise/.github/workflows/ci.yml",
        None,
    ),
]

# Inherited record folders: every record in the original folder must exist in
# the copy byte-identically. The copy may hold records of its own on top,
# because a full adaptation records its own decisions in its own sequence.
CARRIED_TREES = [
    (
        "decision records",
        "Keel/docs/decisions",
        "Quiver/arrows/coinwise/docs/decisions",
    ),
]


def cut(text: str, start: str | None, end: str | None) -> str:
    """The block between the anchors, or the whole text when both are None."""
    begin = 0 if start is None else text.index(start)
    stop = len(text) if end is None else text.index(end)
    return text[begin:stop]


def main() -> int:
    """Compare every copy of every shared block and report each divergence."""
    problems: list[str] = []
    for name, files, start, end in BLOCKS:
        digests: dict[str, list[str]] = {}
        for rel in files:
            path = ROOT / rel
            try:
                block = cut(path.read_text(encoding="utf-8"), start, end)
            except FileNotFoundError:
                problems.append(f"{name}: {rel} is missing")
                continue
            except ValueError:
                problems.append(f"{name}: {rel} lacks the anchor that bounds this block")
                continue
            normalized = block.replace("\r\n", "\n")
            digests.setdefault(hashlib.sha256(normalized.encode()).hexdigest(), []).append(rel)
        if len(digests) > 1:
            copies = "; ".join(", ".join(v) for v in digests.values())
            problems.append(f"{name}: the copies diverge ({copies}); align them, they are one law")

    for name, original, copy, start in CARRIES:
        texts: dict[str, str] = {}
        for rel in (original, copy):
            path = ROOT / rel
            try:
                texts[rel] = cut(path.read_text(encoding="utf-8"), start, None).replace("\r\n", "\n")
            except FileNotFoundError:
                problems.append(f"carried {name}: {rel} is missing")
            except ValueError:
                problems.append(f"carried {name}: {rel} lacks the anchor that bounds this block")
        if len(texts) == 2 and texts[original] != texts[copy]:
            problems.append(
                f"carried {name}: {copy} does not match {original};"
                " the original is canonical, rewrite the copy"
            )

    for name, original_dir, copy_dir in CARRIED_TREES:
        for path in sorted((ROOT / original_dir).glob("*.md")):
            twin = ROOT / copy_dir / path.name
            if not twin.exists():
                problems.append(
                    f"carried {name}: {copy_dir}/{path.name} is missing;"
                    f" the copy must hold every record of {original_dir}"
                )
            elif twin.read_text(encoding="utf-8").replace("\r\n", "\n") != path.read_text(
                encoding="utf-8"
            ).replace("\r\n", "\n"):
                problems.append(
                    f"carried {name}: {copy_dir}/{path.name} does not match its original;"
                    " an inherited record is immutable in the copy"
                )

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The family's shared law has drifted.")
        return 1
    print("The family's shared law is one text and every carried copy matches its original.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
