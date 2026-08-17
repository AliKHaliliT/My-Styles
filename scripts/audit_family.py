"""Audit the family's shared law for drift between the styles.

The styles replicate certain blocks of law by hand: the delivery gate and the
upstream report in each agent guide, the rulebook's shared core, and the docs
audit the two Python styles carry as one script. Replication without drift
detection is the failure mode this family refuses to tolerate in its derived
projects, so the same standard applies here. The manifest below is also the
blueprint: when a new style joins the family, the blocks named here are what
it must carry, and adding it to the file lists is what puts it under guard.

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
        ["ArchtypeCore/AGENTS.md", "Keel/AGENTS.md", "Helm/AGENTS.md"],
        "## The upstream report",
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

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The family's shared law has drifted.")
        return 1
    print("The family's shared law is one text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
