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

The third duty is the root's own workflow, which no seat's audit reads: every
action it uses from another repository is pinned to a commit with its version
named beside it, the rule each seat's docs audit holds for the seat's own
workflow. Run with --selftest to see that rule fire against a planted tag.
"""

import hashlib
import re
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
# anchor, end anchor), None standing for the file's edge. The guide's tail stops
# before the documentation index, because the index lists the arrow's own
# documents. The original is canonical; a divergence is fixed by rewriting the
# copy, never the original.
CARRIES = [
    (
        "agent guide shared tail",
        "Keel/AGENTS.md",
        "Quiver/arrows/coinwise/AGENTS.md",
        "The checks report at two levels",
        "## Documentation index",
    ),
    (
        "rulebook",
        "Keel/docs/CONVENTIONS.md",
        "Quiver/arrows/coinwise/docs/CONVENTIONS.md",
        None,
        None,
    ),
    (
        "baseline",
        "Keel/docs/BASELINE.md",
        "Quiver/arrows/coinwise/docs/BASELINE.md",
        None,
        None,
    ),
    (
        "docs audit",
        "Keel/scripts/audit_docs.py",
        "Quiver/arrows/coinwise/scripts/audit_docs.py",
        None,
        None,
    ),
    (
        ".gitignore",
        "Keel/.gitignore",
        "Quiver/arrows/coinwise/.gitignore",
        None,
        None,
    ),
    (
        ".gitattributes",
        "Keel/.gitattributes",
        "Quiver/arrows/coinwise/.gitattributes",
        None,
        None,
    ),
    (
        ".editorconfig",
        "Keel/.editorconfig",
        "Quiver/arrows/coinwise/.editorconfig",
        None,
        None,
    ),
    (
        "inert workflow",
        "Keel/.github/workflows/ci.yml",
        "Quiver/arrows/coinwise/.github/workflows/ci.yml",
        None,
        None,
    ),
]

# Inherited record folders: the copy is the original folder whole, every record
# byte-identical and nothing else beside them, because an arrow's own decisions
# live in its own decisions folder from 0001 and never mix with the style's.
CARRIED_TREES = [
    (
        "decision records",
        "Keel/docs/decisions",
        "Quiver/arrows/coinwise/docs/inherited",
    ),
]


def cut(text: str, start: str | None, end: str | None) -> str:
    """The block between the anchors, or the whole text when both are None."""
    begin = 0 if start is None else text.index(start)
    stop = len(text) if end is None else text.index(end)
    return text[begin:stop]


def check_blocks(problems: list[str]) -> None:
    """Every copy of every shared block is one text."""
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


def check_carries(problems: list[str]) -> None:
    """Every block an arrow carries from its style matches the original."""
    for name, original, copy, start, end in CARRIES:
        texts: dict[str, str] = {}
        for rel in (original, copy):
            path = ROOT / rel
            try:
                texts[rel] = cut(path.read_text(encoding="utf-8"), start, end).replace("\r\n", "\n")
            except FileNotFoundError:
                problems.append(f"carried {name}: {rel} is missing")
            except ValueError:
                problems.append(f"carried {name}: {rel} lacks the anchor that bounds this block")
        if len(texts) == 2 and texts[original] != texts[copy]:
            problems.append(
                f"carried {name}: {copy} does not match {original};"
                " the original is canonical, rewrite the copy"
            )


def check_carried_trees(problems: list[str]) -> None:
    """Every inherited folder is the original folder whole, record for record, and nothing more."""
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
        originals = {p.name for p in (ROOT / original_dir).glob("*.md")}
        for extra in sorted((ROOT / copy_dir).glob("*.md")):
            if extra.name not in originals:
                problems.append(
                    f"carried {name}: {copy_dir}/{extra.name} is not a record of {original_dir};"
                    " the inherited folder is the original whole, and the copy's own records live in its decisions folder"
                )


# An action a workflow uses from another repository names the commit it runs, forty hex characters,
# with its version in the comment beside it, because a tag is a name that moves. A local action,
# a path beginning with ./, and a container image, docker://, name no ref in another repository.
USES_LINE = re.compile(r"^\s*-?\s*uses:\s*(\S+)(.*)$")
PINNED_USES = re.compile(r"^[^@]+@[0-9a-f]{40}$")
VERSION_COMMENT = re.compile(r"^\s+#\s*v?\d")


def workflow_files(root: Path) -> list[Path]:
    """Every workflow file in the tree's .github/workflows folder, in name order."""
    folder = root / ".github/workflows"
    if not folder.is_dir():
        return []
    return sorted(path for path in folder.iterdir() if path.suffix in (".yml", ".yaml") and path.is_file())


def check_action_pins(problems: list[str], root: Path) -> None:
    """Every action a workflow uses from another repository is pinned to a commit, with its version named beside it."""
    for path in workflow_files(root):
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            match = USES_LINE.match(line)
            if match is None:
                continue
            reference, tail = match.group(1).strip("'\""), match.group(2)
            if reference.startswith(("./", "docker://")):
                continue
            if not PINNED_USES.match(reference):
                problems.append(
                    f"{rel}:{number}: {reference} is pinned by a name that can move; an action from another repository"
                    " names the commit it runs, forty hex characters, with its version in a comment beside it"
                )
            elif not VERSION_COMMENT.match(tail):
                problems.append(f"{rel}:{number}: {reference} names its commit and not its version; the comment beside the pin says which release the commit is")


def prove_action_pins() -> int:
    """A planted tag and a planted pin without its version each raise their finding, and the plant leaves."""
    failures = 0
    for rel, content, needle in (
        (".github/workflows/PLANTED.yml", "on: push\njobs:\n  planted:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v7\n", ".github/workflows/PLANTED.yml:6: actions/checkout@v7 is pinned by a name that can move"),
        (".github/workflows/PLANTED.yml", "on: push\njobs:\n  planted:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n", ".github/workflows/PLANTED.yml:6: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 names its commit and not its version"),
    ):
        target = ROOT / rel
        target.write_text(content, encoding="utf-8")
        try:
            problems: list[str] = []
            check_action_pins(problems, ROOT)
            if not any(needle in p for p in problems):
                print(f"WRONG: plant {rel} did not raise {needle!r}")
                failures += 1
        finally:
            target.unlink()
    return failures


def selftest() -> int:
    """The pin rule fires on each planted defect."""
    failures = prove_action_pins()
    if failures:
        print(f"{failures} rule(s) did not fire.")
        return 1
    print("The family audit's pin rule fires on every planted defect.")
    return 0


def main() -> int:
    """Compare every copy of every shared block, hold the root's workflow to its pins, and report each divergence."""
    if "--selftest" in sys.argv:
        return selftest()
    problems: list[str] = []
    check_blocks(problems)
    check_carries(problems)
    check_carried_trees(problems)
    check_action_pins(problems, ROOT)

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The family's shared law has drifted.")
        return 1
    print("The family's shared law is one text and every carried copy matches its original.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
