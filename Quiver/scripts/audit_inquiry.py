"""Audit the inquiry layer against its own rules.

The mechanical half of the rulebook is checked here: document shapes and
budgets, the registration index over the whole docs zone, the relative links
and root-anchored paths living documents name, the room every root entry has
in the map or the baseline, the claim ledger, the immutability of records,
the agreement of figures two claims quote for one run, the citation keys, the
arrow manifests, and the pins against git history. Everything a tool cannot decide, whether a boundary
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
# In-flight work that has not moved in this long is either finished or stalled, and Now is
# for neither; the shorter horizon is what makes the sweep mechanical where it can be.
NOW_HORIZON_DAYS = 30
NOW_CAP = 5
RECORD_FOLDERS = ("docs/decisions", "docs/claims")

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
# A figure a claim rests on, written on its own line so two records can be held to one value.
FIGURE = re.compile(r"^figure ([a-z0-9_-]+): (.+?)\s*$", re.MULTILINE)
# A changed diff line that is not a Status line; the +++ and --- headers are excluded by the
# lookahead and skipped by name where the diff is read.
ILLEGAL_RECORD_EDIT = re.compile(r"^[-+](?![-+])(?!Status: )")
# A name that stands before a slash anywhere in the map or the baseline is a housed directory.
HOUSED = re.compile(r"([A-Za-z0-9_.-]+)/")


def git(*args: str) -> str:
    """One git call against the repository this file lives in."""
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return done.stdout.strip() if done.returncode == 0 else ""


def tracked_files() -> list[str]:
    """Every tracked path, posix and relative to the root, so untracked local clutter never fires a check."""
    return [p for p in git("ls-files", "-z").split("\0") if p]


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
        section = ""
        today = datetime.now(timezone.utc).date()
        for raw in text.split("\n"):
            if raw.startswith("## "):
                section = raw[3:].strip()
                continue
            if not raw.startswith("- ") or "Nothing" in raw:
                continue
            stamp = STATE_DATE.search(raw)
            horizon = NOW_HORIZON_DAYS if section == "Now" else HORIZON_DAYS
            if not stamp:
                problems.append(f"STATE.md: entry lacks a date: {raw.strip()[:60]}")
            elif (today - date.fromisoformat(stamp.group(1))).days > horizon:
                problems.append(f"STATE.md: entry past the {horizon}-day horizon of {section}: {raw.strip()[:60]}")
    # Everything else under docs/ is a document with a room or it does not exist. A file below
    # a subdirectory is registered by its own path or by its directory's row in the index; a
    # file that is not markdown has no species and no room here at all.
    for tracked in tracked_files() if root == ROOT else []:
        if not tracked.startswith("docs/") or tracked.startswith(("docs/decisions/", "docs/claims/")):
            continue
        if tracked.count("/") == 1 and tracked.endswith(".md"):
            continue
        folder = "/".join(tracked.split("/")[:2])
        if not tracked.endswith(".md"):
            problems.append(f"{tracked}: docs/ holds markdown documents only; assets live where the baseline sends them")
        elif f"({tracked})" not in rows and f"({folder}/)" not in rows:
            problems.append(f"{tracked}: lives under docs/ but is neither the spine, a record, nor registered in the index; give it a room or fold it")


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


def check_rooms(problems: list[str], root: Path) -> None:
    """Every tracked root directory and root file has a room in the map or the baseline.

    The inquiry layer draws no package tree, so a directory is housed when its name stands
    before a slash anywhere in docs/ARCHITECTURE.md or docs/BASELINE.md, and a root file when
    either names it in backticks. Deeper structure belongs to the arrows and their own law.
    """
    if root != ROOT:
        return
    named: set[str] = set()
    for rel in ("docs/ARCHITECTURE.md", "docs/BASELINE.md"):
        if (root / rel).exists():
            text = (root / rel).read_text(encoding="utf-8")
            named.update(HOUSED.findall(text))
            for match in PATH_TOKEN.finditer(text):
                named.update(seg for seg in match.group(1).removeprefix("./").split("/") if seg)
    directories = {p.split("/")[0] for p in tracked_files() if "/" in p}
    files = {p for p in tracked_files() if "/" not in p} - {"AGENTS.md", "README.md", "STATE.md", "LICENSE"}
    problems.extend(
        f"{d}/: exists in the tree but has no room in docs/ARCHITECTURE.md or the baseline; draw it or fold it"
        for d in sorted(directories) if d not in named
    )
    problems.extend(
        f"{f}: sits at the root but neither the map nor the baseline names it; give it a room or remove it"
        for f in sorted(files) if f not in named
    )


def check_record_immutability(problems: list[str], root: Path) -> None:
    """A record changes only on its Status line, in the working tree and in every commit since this check arrived.

    The rule binds from the commit that brought this check into the tree, found in git's own
    history, so an adopting project is held from its adoption forward and never re-litigates a
    past it did not write under the rule. A shallow clone cannot show that history, so it fails
    rather than quietly checking less.
    """
    if root != ROOT:
        return
    if git("rev-parse", "--is-shallow-repository") == "true":
        problems.append("the clone is shallow, so record history cannot be checked; fetch the full history")
        return
    arrivals = git("log", "--reverse", "--format=%H", "-S", "def check_record_immutability", "--", "scripts/audit_inquiry.py").split()
    diffs = [("the working tree", git("diff", "HEAD", "--unified=0", "--diff-filter=M", "--", *RECORD_FOLDERS))]
    if arrivals:
        commits = [arrivals[0], *git("log", "--format=%H", f"{arrivals[0]}..HEAD", "--diff-filter=M", "--", *RECORD_FOLDERS).split()]
        diffs.extend(
            (sha[:12], git("show", sha, "--format=", "--unified=0", "-M", "--diff-filter=M", "--", *RECORD_FOLDERS))
            for sha in commits
        )
    for where, diff in diffs:
        current = ""
        flagged: set[str] = set()
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                current = line[6:]
                continue
            if line.startswith(("--- ", "+++ ", "@@", "diff ", "index ", "similarity ", "rename ")):
                continue
            if ILLEGAL_RECORD_EDIT.match(line) and current not in flagged:
                flagged.add(current)
                problems.append(f"{current}: edited beyond its Status line in {where}; a record is immutable, so supersede it instead")


def check_figures(problems: list[str], root: Path) -> None:
    """Two claims quoting the same figure at the same pin quote the same value.

    A figure is a `figure <name>: <value>` line in a claim, and it is held against every pin
    the claim names, so a record that cites one run and quotes another's number, or two records
    that disagree about one run, fails here instead of waiting for a reader to notice.
    """
    seen: dict[tuple[str, str], tuple[str, str]] = {}
    for path in sorted((root / "docs/claims").glob("*.md")) if (root / "docs/claims").exists() else []:
        text = path.read_text(encoding="utf-8")
        pins = [pin for _, pin in PIN.findall(text)]
        for name, value in FIGURE.findall(text):
            for pin in pins:
                key = (pin, name)
                if key in seen and seen[key][0] != value:
                    problems.append(
                        f"docs/claims/{path.name}: figure {name} at pin {pin[:12]} is {value}, but "
                        f"{seen[key][1]} quotes {seen[key][0]}; two records quote different values for one run"
                    )
                seen.setdefault(key, (value, path.name))


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
    # A manifest is living, so the claims it says rest on the arrow are the current ones: every
    # claim still standing that pins the arrow is linked, and no superseded claim is.
    for name in sorted(arrows & manifests):
        manifest = (root / "docs/arrows" / f"{name}.md").read_text(encoding="utf-8")
        for path in sorted((root / "docs/claims").glob("*.md")) if (root / "docs/claims").exists() else []:
            text = path.read_text(encoding="utf-8")
            if not any(arrow == name for arrow, _ in PIN.findall(text)):
                continue
            superseded = any(l.startswith("Status: Superseded by") for l in text.split("\n"))
            linked = path.name in manifest
            if superseded and linked:
                problems.append(f"docs/arrows/{name}.md: still lists {path.name}, which is superseded; a manifest names the current claims")
            if not superseded and not linked:
                problems.append(f"docs/arrows/{name}.md: does not list {path.name}, a current claim pinned to this arrow")


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
    check_rooms(problems, root)
    check_records(problems, root)
    check_record_immutability(problems, root)
    check_figures(problems, root)
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
    ("docs/claims/0095-planted-unlisted.md",
     "# 0095. Planted unlisted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nrun at arrows/coinwise at 0123456789ab.\n\n## Threats\n\n- None named.\n",
     "does not list 0095-planted-unlisted.md, a current claim pinned to this arrow"),
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


# Plants the tracked-tree checks can see; each is intent-to-added for one run.
TRACKED_PLANTS = [
    ("docs/legacy/OLD.md", "# Old\n", "neither the spine, a record, nor registered in the index"),
    ("docs/diagram.png", "not a document\n", "docs/ holds markdown documents only"),
    ("stray/note.txt", "nobody gave this a room\n", "stray/: exists in the tree but has no room"),
    ("ROGUE.txt", "nobody named this\n", "ROGUE.txt: sits at the root but neither the map nor the baseline names it"),
]

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
    # Checks that read the tracked tree need a plant git can see, so these are added with
    # intent-to-add and removed from the index again; nothing reaches a commit.
    for rel, content, expect in TRACKED_PLANTS:
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        git("add", "-N", "--", rel)
        try:
            tracked_problems, _ = run(ROOT)
            if not any(expect in p for p in tracked_problems):
                failures += 1
                print(f"WRONG: tracked plant {rel} did not raise {expect!r}")
        finally:
            git("rm", "--cached", "-q", "--", rel)
            target.unlink()
            if target.parent != ROOT and not any(target.parent.iterdir()):
                target.parent.rmdir()
    # Two claims quoting one figure at one pin must agree, so the plant is a pair.
    pair = [
        ("docs/claims/0094-planted-figure-a.md", "0094", "5.000"),
        ("docs/claims/0093-planted-figure-b.md", "0093", "6.000"),
    ]
    written = []
    try:
        for rel, num, value in pair:
            target = ROOT / rel
            target.write_text(
                f"# {num}. Planted figure\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n"
                f"## Evidence\n\nrun at arrows/coinwise at 0123456789ab.\n\nfigure drift: {value}\n\n## Threats\n\n- None named.\n",
                encoding="utf-8",
            )
            written.append(target)
        figure_problems, _ = run(ROOT)
        if not any("two records quote different values" in p for p in figure_problems):
            failures += 1
            print("WRONG: two claims quoting different values for one figure at one pin raised nothing")
    finally:
        for target in written:
            target.unlink()
    # A record edited beyond its Status line must fail, and a Status flip alone must pass, or
    # the check would forbid the one edit the rulebook allows.
    record = next(iter(sorted((ROOT / "docs/decisions").glob("0001-*.md"))), None)
    if record is None:
        print("immutability plants skipped: no record 0001 to plant on")
    else:
        original = record.read_bytes()
        try:
            record.write_bytes(original + b"\nplanted body edit\n")
            edited_problems, _ = run(ROOT)
            if not any("edited beyond its Status line" in p for p in edited_problems):
                failures += 1
                print(f"WRONG: a body edit to {record.name} raised nothing")
            record.write_bytes(original.replace(b"Status: Accepted", b"Status: Superseded by 0099", 1))
            flipped_problems, _ = run(ROOT)
            if any("edited beyond its Status line" in p for p in flipped_problems):
                failures += 1
                print(f"WRONG: a Status flip on {record.name} was reported as an illegal edit")
        finally:
            record.write_bytes(original)
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
