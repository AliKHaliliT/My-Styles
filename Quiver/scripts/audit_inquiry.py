"""Audit the inquiry layer against its own rules.

The mechanical half of the rulebook is checked here: document shapes and
budgets, the registration index, the relative links and root-anchored paths
living documents name, the claim ledger, the citation keys, the arrow
manifests, and the pins against git history. Everything a tool cannot decide, whether a boundary
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
from datetime import date, datetime, timezone
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
# A key is an author name closed by a year, or a standard's designation with
# its year suffixed, so digits may sit inside the name (ieee754-2019).
CITE_KEY = re.compile(r"\[([a-z][a-z0-9]*[0-9]{4}[a-z]?|[a-z][a-z0-9]*-[0-9]{4})\](?!\()")
BIB_ENTRY = re.compile(r"^- \*\*([a-z][a-z0-9]*[0-9]{4}[a-z]?|[a-z][a-z0-9]*-[0-9]{4})\*\*:")
PIN = re.compile(r"arrows/([a-z0-9-]+) at ([0-9a-f]{7,40})\b")
LINK = re.compile(r"\]\(([^)\s]+)\)")
PATH_TOKEN = re.compile(r"`([^`\n]+)`")


def git(*args: str) -> str:
    """One git call against the repository this file lives in."""
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return done.stdout.strip() if done.returncode == 0 else ""


def living_documents(root: Path) -> list[str]:
    """The spine plus the enumerable organic zone: docs/*.md and the arrow manifests.

    Records under docs/decisions/ and docs/claims/ describe the past, are exempt
    from every living-document rule, and are shaped by their own checks instead.
    """
    rels = list(LIVING)
    if (root / "docs").exists():
        for path in sorted((root / "docs").glob("*.md")):
            rel = f"docs/{path.name}"
            if rel not in rels:
                rels.append(rel)
    if (root / "docs/arrows").exists():
        rels.extend(f"docs/arrows/{path.name}" for path in sorted((root / "docs/arrows").glob("*.md")))
    return rels


def index_rows(agents: str) -> str:
    """The documentation index table alone, because registration means a row there."""
    if "## Documentation index" not in agents:
        return ""
    return agents.split("## Documentation index", 1)[1].split("\n## ", 1)[0]


def check_living(problems: list[str], root: Path) -> None:
    """Budgets, presence, index registration, and the STATE schema."""
    agents = (root / "AGENTS.md").read_text(encoding="utf-8") if (root / "AGENTS.md").exists() else ""
    rows = index_rows(agents)
    for rel in living_documents(root):
        path = root / rel
        if not path.exists():
            problems.append(f"{rel}: missing living document")
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        if rel not in FREE_GROWING and len(lines) > BUDGET_LINES:
            problems.append(f"{rel}: {len(lines)} lines, budget is {BUDGET_LINES}")
        # The manifests are registered as a folder, one row covering the set.
        registered = f"({rel})" in rows or (rel.startswith("docs/arrows/") and "(docs/arrows/)" in rows)
        if rel not in ("AGENTS.md", "README.md") and not registered:
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
            elif (datetime.now(timezone.utc).date() - date.fromisoformat(stamp.group(1))).days > HORIZON_DAYS:
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
                # A superseded record is exempt on both sides. Its evidence lives in
                # its superseder, because immutability forbids a conjecture ever
                # gaining evidence in place. The owner approved this rule after the
                # check wrongly failed the first settled conjecture.
                is_superseded = any(l.startswith("Status: Superseded by") for l in lines)
                if is_conjecture and body != "None.":
                    problems.append(f"{rel}: a Conjecture carries evidence; support it or empty it")
                if not is_conjecture and not is_superseded and body == "None.":
                    problems.append(f"{rel}: a settled claim has no evidence")
                if any(l.startswith("Status: Refuted") for l in lines) and "eopen" not in text:
                    problems.append(f"{rel}: a Refuted claim names no reopening condition")


def claims_to_be_path(token: str, root: Path) -> bool:
    """Whether a backticked token is claiming to be a repository path.

    Only tokens rooted in something the repository root knows are checked; an
    unknown first segment is prose, not a path (placeholders, media types).
    """
    if "/" not in token or " " in token:
        return False
    if any(ch in token for ch in "<>*{}$|\\=\"'"):
        return False
    if "://" in token or token.startswith(("http", "-", "@")):
        return False
    first = token.lstrip("./").split("/")[0]
    return (root / first).exists()


def check_references(problems: list[str], root: Path) -> None:
    """Every relative link in a living document resolves, and every root-anchored path it names exists."""
    for rel in living_documents(root):
        path = root / rel
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for target in LINK.findall(line):
                bare = target.split("#", 1)[0]
                if not bare or "://" in bare or bare.startswith("mailto:"):
                    continue
                if not (path.parent / bare).exists():
                    problems.append(f"{rel}:{line_no}: links to {target}, which does not resolve")
            for token in PATH_TOKEN.findall(line):
                if claims_to_be_path(token, root) and not (root / token).exists():
                    problems.append(f"{rel}:{line_no}: names `{token}`, which does not exist")


def check_citations(problems: list[str], root: Path) -> None:
    """Every cited key resolves in the bibliography."""
    bib = root / "docs/BIBLIOGRAPHY.md"
    keys = set()
    if bib.exists():
        for line in bib.read_text(encoding="utf-8").split("\n"):
            entry = BIB_ENTRY.match(line)
            if entry:
                keys.add(entry.group(1))
    sources = [*(root / rel for rel in living_documents(root)),
               *sorted((root / "docs/claims").glob("*.md")),
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


# The paths inside an arrow that can change what a run produces: the code, the
# suites, and the project file that selects dependencies and warning behavior.
# Documentation and workflow bytes carried inside an arrow execute nothing
# during an experiment, so their movement can move no number and never advises.
EVIDENCE_PATHS = ("src", "tests", "pyproject.toml")


def check_pins(problems: list[str], advice: list[str], root: Path) -> None:
    """Pins exist in history; movement past a pin is advice, never a verdict."""
    for path in sorted((root / "docs/claims").glob("*.md")):
        rel = f"docs/claims/{path.name}"
        text = path.read_text(encoding="utf-8")
        # A claim whose status already says it is not current, Stale or Superseded,
        # leaves the movement advisory nothing to prompt, so only claims still
        # standing as current are advised. The pin must be a real commit either
        # way, because a record's evidence never gets to point at nothing.
        resting = any(
            l.startswith(("Status: Stale", "Status: Superseded by")) for l in text.split("\n")
        )
        for arrow, pin in PIN.findall(text):
            if not git("rev-parse", "--verify", f"{pin}^{{commit}}"):
                problems.append(f"{rel}: pin {pin} is not a commit in this history")
                continue
            if resting:
                continue
            spec = [f"arrows/{arrow}/{part}" for part in EVIDENCE_PATHS]
            moved = git("log", "--oneline", f"{pin}..HEAD", "--", *spec)
            if moved:
                advice.append(
                    f"{rel}: arrows/{arrow} evidence paths moved past pin {pin[:12]}"
                    f" ({len(moved.splitlines())} commit(s)); confirm the claim or flip it Stale"
                )


def run(root: Path) -> tuple[list[str], list[str]]:
    """Every decided problem and every piece of advice for one tree."""
    problems: list[str] = []
    advice: list[str] = []
    check_living(problems, root)
    check_references(problems, root)
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
    ("docs/claims/0011-planted.md",
     "# 0011. Planted\n\nStatus: Conjecture\nDate: 2026-01-01\n\n## Claim\n\ncites [fake754-2019].\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "[fake754-2019] not in the bibliography"),
    ("docs/arrows/ghost.md", "# Arrow: ghost\n", "manifest for an arrow that does not exist"),
    ("docs/PLANTED.md", "# Planted\n\nAn organic document nobody registered.\n",
     "docs/PLANTED.md: not registered in the AGENTS.md index"),
    ("docs/PLANTED.md", "# Planted\n\n[gone](ghost/none.md)\n", "links to ghost/none.md, which does not resolve"),
    ("docs/PLANTED.md", "# Planted\n\nNames `docs/ghost-none.md` in passing.\n",
     "names `docs/ghost-none.md`, which does not exist"),
    ("docs/PLANTED.md", "# Planted\n" + "line\n" * 151, "budget is 150"),
]

def moved_evidence_pin() -> tuple[str, str] | None:
    """An arrow and a commit its evidence paths moved past, or None when none has."""
    if not (ROOT / "arrows").exists():
        return None
    for path in sorted((ROOT / "arrows").iterdir()):
        if not path.is_dir():
            continue
        spec = [f"arrows/{path.name}/{part}" for part in EVIDENCE_PATHS]
        shas = git("log", "--reverse", "--format=%H", "--", *spec).split("\n")
        if len(shas) >= 2 and shas[0]:
            return path.name, shas[0]
    return None


def docs_only_moved_pin() -> tuple[str, str] | None:
    """An arrow and a commit it moved past in non-evidence bytes alone, or None."""
    if not (ROOT / "arrows").exists():
        return None
    for path in sorted((ROOT / "arrows").iterdir()):
        if not path.is_dir():
            continue
        spec = [f"arrows/{path.name}/{part}" for part in EVIDENCE_PATHS]
        last_evidence = git("log", "-1", "--format=%H", "--", *spec)
        if not last_evidence:
            continue
        # Every commit past the last evidence commit that touched the arrow
        # touched only its other bytes, or it would itself be the last one.
        if git("log", "--oneline", f"{last_evidence}..HEAD", "--", f"arrows/{path.name}"):
            return path.name, last_evidence
    return None


# A superseded conjecture keeps Evidence None. and must PASS, or this checker
# would force evidence into an immutable record to earn a clean run.
LEGAL_PLANTS = [
    ("docs/claims/0005-planted-legal.md",
     ("# 0005. Planted legal\n\nStatus: Superseded by 0002\nDate: 2026-01-01\n\n"
      "## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n")),
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
    for rel, content in LEGAL_PLANTS:
        target = ROOT / rel
        target.write_text(content, encoding="utf-8")
        try:
            legal_problems, _ = run(ROOT)
            if legal_problems:
                failures += 1
                print(f"WRONG: legal plant {rel} raised {legal_problems[:2]}")
        finally:
            target.unlink()
    body = (
        "# {num}. Planted advisory\n\nStatus: {status}\nDate: 2026-01-01\n\n"
        "## Claim\n\nx.\n\n## Evidence\n\n{evidence}\n\n## Threats\n\n- None named.\n"
    )
    mover = moved_evidence_pin()
    if mover is None:
        print("advisory plants skipped: no arrow's evidence paths have moved in this history")
    else:
        arrow_name, old_pin = mover
        pinned = f"run at arrows/{arrow_name} at {old_pin}."
        movers: list[tuple[str, str, str, str, bool]] = [
            ("docs/claims/0099-planted-moving.md", "0099", "Supported", pinned, True),
            ("docs/claims/0098-planted-resting.md", "0098", "Stale", pinned, False),
            ("docs/claims/0097-planted-passed.md", "0097", "Superseded by 0099", pinned, False),
        ]
        targets = []
        try:
            for rel, num, status, evidence, _expect in movers:
                target = ROOT / rel
                target.write_text(
                    body.format(num=num, status=status, evidence=evidence), encoding="utf-8"
                )
                targets.append(target)
            _, moved_advice = run(ROOT)
            for rel, num, status, _evidence, should_fire in movers:
                fired = any(rel in a for a in moved_advice)
                if fired != should_fire:
                    failures += 1
                    verb = "did not raise" if should_fire else "wrongly raised"
                    print(f"WRONG: plant {rel} ({status}) {verb} the movement advisory")
        finally:
            for target in targets:
                target.unlink()
    quiet_mover = docs_only_moved_pin()
    if quiet_mover is None:
        print("docs-only advisory plant skipped: no arrow has moved in non-evidence bytes alone")
    else:
        arrow_name, quiet_pin = quiet_mover
        rel = "docs/claims/0096-planted-quiet.md"
        target = ROOT / rel
        target.write_text(
            body.format(
                num="0096",
                status="Supported",
                evidence=f"run at arrows/{arrow_name} at {quiet_pin}.",
            ),
            encoding="utf-8",
        )
        try:
            _, quiet_advice = run(ROOT)
            if any(rel in a for a in quiet_advice):
                failures += 1
                print(f"WRONG: plant {rel} raised the movement advisory for a docs-only move")
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
