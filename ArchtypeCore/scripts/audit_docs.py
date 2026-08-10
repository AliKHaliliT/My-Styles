"""Audit the living documents for the three kinds of rot they can carry.

A living document rots when a sentence that was true at writing stops being true after
reality moves through a path that never touches the file. The mechanical kinds are checked
here; the docs rulebook carries the rest. Decision records are exempt because they describe
the past, which does not rot.
"""

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LIVING = [
    "AGENTS.md",
    "README.md",
    "STATE.md",
    "docs/ARCHITECTURE.md",
    "docs/BASELINE.md",
    "docs/CONVENTIONS.md",
]

# An entry older than this is expired and must be re-verified before anything relies on it.
HORIZON_DAYS = 90

BACKTICK = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")


def looks_like_path(token: str) -> bool:
    """Whether a backticked token is claiming to be a repository path."""
    if "/" not in token or " " in token:
        return False
    if any(ch in token for ch in "<>*{}$|\\=\"'"):
        return False
    if "://" in token or token.startswith(("http", "-", "@")):
        return False
    # Only claims rooted in something that exists at the repository root are checked;
    # a first segment the root does not know is prose, not a path (media types, examples).
    first = token.lstrip("./").split("/")[0]
    return (ROOT / first).exists()


def main() -> int:
    """Run the three checks over the living documents and report every disagreement."""
    problems: list[str] = []
    today = date.today()

    for rel in LIVING:
        doc = ROOT / rel
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")

        for match in BACKTICK.finditer(text):
            token = match.group(1).strip()
            if looks_like_path(token) and not (ROOT / token.lstrip("./").rstrip("/")).exists():
                line = text.count("\n", 0, match.start()) + 1
                problems.append(f"{rel}:{line}: names `{token}`, which does not exist")

        # Links inside inline code spans are schema examples, not claims; blank the spans
        # with same-length padding so reported line numbers stay true.
        prose = BACKTICK.sub(lambda m: " " * len(m.group(0)), text)
        for match in LINK.finditer(prose):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (doc.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                line = prose.count("\n", 0, match.start()) + 1
                problems.append(f"{rel}:{line}: links to {target}, which does not resolve")

    state = ROOT / "STATE.md"
    if state.exists():
        text = state.read_text(encoding="utf-8")
        for match in STATE_DATE.finditer(text):
            stamped = datetime.strptime(match.group(1), "%Y-%m-%d").date()
            age = (today - stamped).days
            if age > HORIZON_DAYS:
                line = text.count("\n", 0, match.start()) + 1
                problems.append(
                    f"STATE.md:{line}: entry last verified {match.group(1)}, {age} days ago; "
                    f"re-verify it against reality, then re-date or remove it"
                )

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The living documents disagree with reality.")
        return 1
    print("Living documents agree with reality.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
