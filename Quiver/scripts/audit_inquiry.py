"""Audit the inquiry layer against its own rules.

The mechanical half of the rulebook is checked here: document shapes and
budgets, the claim ledger, the citation keys, the arrow manifests, and the
pins against git history. Everything a tool cannot decide, whether a boundary
was the right one, whether a moved arrow touched what a claim measured, is
advised or left to review, because a check may never imply more than it
decides.

Run with --selftest first on any change to this file, because a check that
never fires and a check that cannot fire look identical.
"""

import re
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LIVING = [
    "AGENTS.md",
    "README.md",
    "STATE.md",
    "docs/QUESTION.md",
    "docs/ARCHITECTURE.md",
    "docs/BIBLIOGRAPHY.md",
    "docs/CONVENTIONS.md",
    "docs/BASELINE.md",
]
FREE_GROWING = {"AGENTS.md", "README.md", "docs/ARCHITECTURE.md", "docs/BIBLIOGRAPHY.md"}
BUDGET_LINES = 150
HORIZON_DAYS = 90
NOW_CAP = 5

CLAIM_STATUS = re.compile(r"^Status: (Conjecture|Supported|Refuted|Stale|Superseded by \d{4})$")
DECISION_STATUS = re.compile(r"^Status: (Accepted|Superseded by .+)$")
RECORD_NAME = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
CITE_KEY = re.compile(r"\[([a-z]+[0-9]{4}[a-z]?(?:-[0-9]{4})?)\](?!\()")
BIB_ENTRY = re.compile(r"^- \*\*([a-z]+[0-9]{4}[a-z]?(?:-[0-9]{4})?)\*\*:")
PIN = re.compile(r"arrows/([a-z0-9-]+) at ([0-9a-f]{7,40})\b")


def git(*args: str) -> str:
    """One git call against the repository this file lives in."""
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return done.stdout.strip() if done.returncode == 0 else ""


def check_living(problems: list[str], root: Path) -> None:
    """Budgets, presence, index registration, and the STATE schema."""
    agents = (root / "AGENTS.md").read_text(encoding="utf-8") if (root / "AGENTS.md").exists() else ""
    for rel in LIVING:
        path = root / rel
        if not path.exists():
            problems.append(f"{rel}: missing living document")
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        if rel not in FREE_GROWING and len(lines) > BUDGET_LINES:
            problems.append(f"{rel}: {len(lines)} lines, budget is {BUDGET_LINES}")
        if rel not in ("AGENTS.md", "README.md") and f"({rel})" not in agents:
            problems.append(f"{rel}: not registered in the AGENTS.md index")

    state = root / "STATE.md"
    if state.exists():
        text = state.read_text(encoding="utf-8")
        for section in ("## Now", "## Next", "## Deferred", "## Blocked"):
            if section not in text:
                problems.append(f"STATE.md: section {section!r} missing")
        now = text.split("## Now", 1)[-1].split("##", 1)[0]
        entries = [l for l in now.split("\n") if l.startswith("- ") and "Nothing" not in l]
        if len(entries) > NOW_CAP:
            problems.append(f"STATE.md: Now holds {len(entries)} entries, cap is {NOW_CAP}")
        for entry in entries:
            stamp = STATE_DATE.search(entry)
            if not stamp:
                problems.append(f"STATE.md: entry lacks a date: {entry.strip()[:60]}")
            elif (date.today() - datetime.strptime(stamp.group(1), "%Y-%m-%d").date()).days > HORIZON_DAYS:
                problems.append(f"STATE.md: entry past the {HORIZON_DAYS}-day horizon: {entry.strip()[:60]}")


def check_records(problems: list[str], root: Path) -> None:
    """Names and status lines for both record kinds, and claim shapes."""
    for folder, status in (("docs/decisions", DECISION_STATUS), ("docs/claims", CLAIM_STATUS)):
        for path in sorted((root / folder).glob("*.md")):
            rel = f"{folder}/{path.name}"
            if not RECORD_NAME.match(path.name):
                problems.append(f"{rel}: name breaks NNNN-kebab-title.md")
            text = path.read_text(encoding="utf-8")
            lines = text.split("\n")
            if not any(status.match(l) for l in lines):
                problems.append(f"{rel}: no legal Status line")
            if not any(l.startswith("Date: ") for l in lines):
                problems.append(f"{rel}: no Date line")
            if folder.endswith("claims"):
                for section in ("## Claim", "## Evidence", "## Threats"):
                    if section not in text:
                        problems.append(f"{rel}: section {section!r} missing")
                body = text.split("## Evidence", 1)[-1].split("##", 1)[0].strip()
                is_conjecture = any(l == "Status: Conjecture" for l in lines)
                if is_conjecture and body != "None.":
                    problems.append(f"{rel}: a Conjecture carries evidence; support it or empty it")
                if not is_conjecture and body == "None.":
                    problems.append(f"{rel}: a settled claim has no evidence")
                if any(l.startswith("Status: Refuted") for l in lines) and "eopen" not in text:
                    problems.append(f"{rel}: a Refuted claim names no reopening condition")


def check_citations(problems: list[str], root: Path) -> None:
    """Every cited key resolves in the bibliography."""
    bib = root / "docs/BIBLIOGRAPHY.md"
    keys = set()
    if bib.exists():
        for line in bib.read_text(encoding="utf-8").split("\n"):
            entry = BIB_ENTRY.match(line)
            if entry:
                keys.add(entry.group(1))
    sources = [root / "docs/QUESTION.md", *sorted((root / "docs/claims").glob("*.md")),
               *sorted((root / "docs/decisions").glob("*.md"))]
    for path in sources:
        if not path.exists():
            continue
        for cited in CITE_KEY.findall(path.read_text(encoding="utf-8")):
            if cited not in keys:
                problems.append(f"{path.relative_to(root)}: cited key [{cited}] not in the bibliography")


def check_arrows(problems: list[str], root: Path) -> None:
    """Every arrow has a manifest and every manifest an arrow."""
    arrows = {p.name for p in (root / "arrows").iterdir() if p.is_dir()} if (root / "arrows").exists() else set()
    manifests = {p.stem for p in (root / "docs/arrows").glob("*.md")} if (root / "docs/arrows").exists() else set()
    for name in sorted(arrows - manifests):
        problems.append(f"arrows/{name}: no manifest at docs/arrows/{name}.md")
    for name in sorted(manifests - arrows):
        problems.append(f"docs/arrows/{name}.md: manifest for an arrow that does not exist")


def check_pins(problems: list[str], advice: list[str], root: Path) -> None:
    """Pins exist in history; movement past a pin is advice, never a verdict."""
    for path in sorted((root / "docs/claims").glob("*.md")):
        rel = f"docs/claims/{path.name}"
        for arrow, pin in PIN.findall(path.read_text(encoding="utf-8")):
            if not git("rev-parse", "--verify", f"{pin}^{{commit}}"):
                problems.append(f"{rel}: pin {pin} is not a commit in this history")
                continue
            moved = git("log", "--oneline", f"{pin}..HEAD", "--", f"arrows/{arrow}")
            if moved:
                advice.append(
                    f"{rel}: arrows/{arrow} moved past pin {pin[:12]}"
                    f" ({len(moved.splitlines())} commit(s)); confirm the claim or flip it Stale"
                )


def run(root: Path) -> tuple[list[str], list[str]]:
    """Every decided problem and every piece of advice for one tree."""
    problems: list[str] = []
    advice: list[str] = []
    check_living(problems, root)
    check_records(problems, root)
    check_citations(problems, root)
    check_arrows(problems, root)
    check_pins(problems, advice, root)
    return problems, advice


PLANTS = [
    ("docs/claims/0009-planted.md",
     "# 0009. Planted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "settled claim has no evidence"),
    ("docs/claims/0008-planted.md",
     "# 0008. Planted\n\nStatus: Refuted\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nkilled by y at arrows/coinwise at 0123456789ab.\n\n## Threats\n\n- None named.\n",
     "names no reopening condition"),
    ("docs/claims/0007-planted.md",
     "# 0007. Planted\n\nStatus: Wrong\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "no legal Status line"),
    ("docs/claims/0006-planted.md",
     "# 0006. Planted\n\nStatus: Conjecture\nDate: 2026-01-01\n\n## Claim\n\ncites [nobody9999].\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "not in the bibliography"),
    ("docs/arrows/ghost.md", "# Arrow: ghost\n", "does not exist"),
]


def selftest() -> int:
    """Prove each rule fires against a planted defect, then leave no trace."""
    failures = 0
    for rel, content, expect in PLANTS:
        target = ROOT / rel
        target.write_text(content, encoding="utf-8")
        try:
            problems, _ = run(ROOT)
            if not any(expect in p for p in problems):
                failures += 1
                print(f"WRONG: plant {rel} did not raise {expect!r}")
        finally:
            target.unlink()
    baseline, _ = run(ROOT)
    if baseline:
        failures += 1
        print("WRONG: the unplanted tree is not clean, so plants cannot be trusted:")
        for p in baseline[:5]:
            print(f"  {p}")
    with tempfile.TemporaryDirectory() as scratch:
        empty, _ = run(Path(scratch))
        if not any("missing living document" in p for p in empty):
            failures += 1
            print("WRONG: an empty tree raised no missing-document problem")
    print("every rule fires" if not failures else f"{failures} rule(s) do not work")
    return 1 if failures else 0


def main() -> int:
    """Audit the tree, or prove the audit."""
    if "--selftest" in sys.argv:
        return selftest()
    problems, advice = run(ROOT)
    if advice:
        print(f"advisory, {len(advice)} item(s), decides nothing and gates nothing:")
        for item in advice:
            print(f"  {item}")
    if problems:
        for problem in problems:
            print(problem)
        print(f"\n{len(problems)} problem(s).")
        return 1
    print("The inquiry agrees with its own rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
