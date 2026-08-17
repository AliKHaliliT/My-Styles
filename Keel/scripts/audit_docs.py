"""Audit the tree against its own documentation and layout conventions.

A living document rots when a sentence that was true at writing stops being true after
reality moves through a path that never touches the file. The mechanical kinds of rot are
checked here, along with the shapes the rulebook fixes: budgets, the index contract, names,
the STATE schema, and the Python layout conventions. Decision records are exempt because
they describe the past, which does not rot.
"""

import ast
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
# Now is for in-flight work only; past this many entries the section is accreting, not tracking.
NOW_CAP = 5
# Bounded documents fail past this; AGENTS.md, docs/ARCHITECTURE.md, and README.md are the
# documents that grow with the system instead.
BUDGET_LINES = 150
FREE_GROWING = {"AGENTS.md", "docs/ARCHITECTURE.md", "README.md"}

BACKTICK = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
RECORD_NAME = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
DOTTED_MODULE = re.compile(r"[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)+")
TREE_FILE = re.compile(r"[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)+")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".ruff_cache", ".venv", "dist", "build"}


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


def repo_basenames() -> set[str]:
    """Every file basename in the tree, for verifying names drawn in tree diagrams."""
    names: set[str] = set()
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            names.add(p.name)
    return names


def python_roots() -> list[Path]:
    """The package trees whose layout conventions the audit holds, found by shape."""
    if (ROOT / "app").is_dir():
        return [ROOT / "app"]
    src = ROOT / "src"
    if src.is_dir():
        return [p for p in src.iterdir() if p.is_dir() and not p.name.startswith(".")]
    return []


def check_documents(problems: list[str]) -> None:
    """Paths, links, budgets, and the STATE horizon across the living documents."""
    today = date.today()
    basenames = repo_basenames()
    # Dotted names declared in pyproject.toml or in the code itself (entry-point groups,
    # contract layers) are not module claims, and their own readers verify the real ones.
    pyproject = ROOT / "pyproject.toml"
    declared = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
    for source in ROOT.rglob("*.py"):
        if not any(part in SKIP_DIRS for part in source.parts):
            declared += source.read_text(encoding="utf-8", errors="ignore")
    for rel in LIVING:
        doc = ROOT / rel
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")

        if rel not in FREE_GROWING:
            lines = text.count("\n") + 1
            if lines > BUDGET_LINES:
                problems.append(f"{rel}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")

        for match in BACKTICK.finditer(text):
            token = match.group(1).strip()
            if looks_like_path(token) and not (ROOT / token.lstrip("./").rstrip("/")).exists():
                line = text.count("\n", 0, match.start()) + 1
                problems.append(f"{rel}:{line}: names `{token}`, which does not exist")
            elif DOTTED_MODULE.fullmatch(token) and token not in declared:
                for root in python_roots():
                    if token.split(".")[0] != root.name:
                        continue
                    module_path = root.parent.joinpath(*token.split("."))
                    if not (module_path.is_dir() or module_path.with_suffix(".py").exists()):
                        line = text.count("\n", 0, match.start()) + 1
                        problems.append(f"{rel}:{line}: names the module `{token}`, which does not exist")

        for fence in FENCE.finditer(text):
            block = fence.group(1)
            if "──" not in block:
                continue
            block_line = text.count("\n", 0, fence.start()) + 1
            for offset, raw in enumerate(block.splitlines()):
                entry = raw.split("#", 1)[0].strip(" │├└─\t").rstrip("/")
                if entry and TREE_FILE.fullmatch(entry) and entry not in basenames:
                    problems.append(
                        f"{rel}:{block_line + offset + 1}: the tree names {entry}, "
                        f"which exists nowhere in this repository"
                    )

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
        sections = re.findall(r"^## (.+)$", text, re.MULTILINE)
        if sections != ["Now", "Next", "Deferred", "Blocked"]:
            problems.append(f"STATE.md: sections are {sections}, not the four the schema fixes")
        for match in STATE_DATE.finditer(text):
            stamped = datetime.strptime(match.group(1), "%Y-%m-%d").date()
            age = (today - stamped).days
            if age > HORIZON_DAYS:
                line = text.count("\n", 0, match.start()) + 1
                problems.append(
                    f"STATE.md:{line}: entry last verified {match.group(1)}, {age} days ago; "
                    f"re-verify it against reality, then re-date or remove it"
                )
        now_section = re.search(r"^## Now\n(.*?)(?=^## )", text, re.MULTILINE | re.DOTALL)
        if now_section:
            entries = len(re.findall(r"^- ", now_section.group(1), re.MULTILINE))
            if entries > NOW_CAP:
                problems.append(
                    f"STATE.md: Now holds {entries} entries against the cap of {NOW_CAP}; "
                    f"sweep finished work into git's memory"
                )


def check_docs_zone(problems: list[str]) -> None:
    """The index contract, budgets, and naming for everything under docs/."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
    for f in sorted(docs.glob("*.md")):
        if f.name not in agents:
            problems.append(f"docs/{f.name}: not registered in the AGENTS.md index")
        if not f.stem.replace("-", "").isupper():
            problems.append(f"docs/{f.name}: organic documents are UPPERCASE markdown")
        if f.name not in ("ARCHITECTURE.md", "CONVENTIONS.md", "BASELINE.md"):
            lines = f.read_text(encoding="utf-8").count("\n") + 1
            if lines > BUDGET_LINES:
                problems.append(f"docs/{f.name}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")
    decisions = docs / "decisions"
    if decisions.is_dir():
        numbers: dict[str, str] = {}
        for f in sorted(decisions.glob("*.md")):
            if not RECORD_NAME.match(f.name):
                problems.append(f"docs/decisions/{f.name}: records are named NNNN-short-kebab-title.md")
                continue
            num = f.name[:4]
            if num in numbers:
                problems.append(
                    f"docs/decisions/: {numbers[num]} and {f.name} share the number {num}; renumber the newer record"
                )
            numbers[num] = f.name


def check_layout(problems: list[str]) -> None:
    """Folder purity and door-only __init__ files, the Python layout conventions."""
    for root in python_roots():
        for directory in [root, *[p for p in root.rglob("*") if p.is_dir()]]:
            if directory.name == "__pycache__":
                continue
            subpackages = [
                p for p in directory.iterdir()
                if p.is_dir() and p.name != "__pycache__" and any(p.rglob("*.py"))
            ]
            modules = [p for p in directory.iterdir() if p.suffix == ".py" and p.name != "__init__.py"]
            if subpackages and modules and directory != root:
                rel = directory.relative_to(ROOT)
                problems.append(f"{rel}: holds both subpackages and modules; a directory holds one or the other")

            init = directory / "__init__.py"
            if init.exists() and directory != root:
                tree = ast.parse(init.read_text(encoding="utf-8"))
                for node in tree.body:
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        continue
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                        continue
                    rel = init.relative_to(ROOT)
                    problems.append(f"{rel}: an __init__.py is a door and only re-exports")
                    break


def main() -> int:
    """Run every check and report each disagreement between the tree and its conventions."""
    problems: list[str] = []
    check_documents(problems)
    check_docs_zone(problems)
    check_layout(problems)

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The tree disagrees with its own conventions.")
        return 1
    print("The tree agrees with its own conventions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
