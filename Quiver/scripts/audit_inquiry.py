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
# The numbered record folders; inherited/ exists only in a project built from this template and
# carries the template's own records whole, keeping their numbers.
RECORD_FOLDERS = ("docs/decisions", "docs/inherited", "docs/claims")

CLAIM_STATUS = re.compile(r"^Status: (Conjecture|Supported|Refuted|Stale|Superseded by \d{4})$")
DECISION_STATUS = re.compile(r"^Status: (Accepted|Superseded by .+)$")
RECORD_NAME = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
DATED_RECORD_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")
REVIEW_SECTIONS = ("## Slice", "## Boundary", "## Method", "## Stages", "## Found", "## Changed", "## Left out")
REVIEW_STAGES = ("Scouting", "Enumeration", "Checks", "Completeness review", "Fold", "Resolution")
STAGE_LINE = re.compile(r"^- (Scouting|Enumeration|Checks|Completeness review|Fold|Resolution): (ran|collapsed)\b(.*)$", re.MULTILINE)
COMPLETENESS = re.compile(r"^Completeness: (exhausted|judgment)\s*$", re.MULTILINE)
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
# A key is an author name closed by a year, or a standard's designation with
# its year suffixed, so digits may sit inside the name (ieee754-2019).
CITE_KEY = re.compile(r"\[([a-z][a-z0-9]*[0-9]{4}[a-z]?|[a-z][a-z0-9]*-[0-9]{4})\](?!\()")
# A key inside backticks names the form and cites nothing, so code spans are blanked before
# citations are read; the rulebook's own example of the form is the case that needs this.
CODE_SPAN = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)
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
# This sentence dates the immutability rule's arrival in the tree's own history, so it is what
# the check searches for, never the function's name, which a child's past may already carry.
# Changing what the check covers changes this sentence, and the anchor moves forward with it.
IMMUTABILITY_SCOPE = "records held immutable beyond their Status line: every file below a subfolder of docs/ except the arrow manifests"


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
    # Below the top level, docs/ holds the record folders and the arrow manifests only. A
    # record folder beyond the numbered ones holds dated documents, registered by its own
    # row; a living document belongs at the top as a flat UPPERCASE file, where the naming and
    # budget rules can see it, so anything else below a subfolder fails.
    for tracked in tracked_files() if root == ROOT else []:
        if not tracked.startswith("docs/") or tracked.startswith(("docs/decisions/", "docs/claims/", "docs/arrows/")):
            continue
        if tracked.count("/") == 1:
            if not tracked.endswith(".md"):
                problems.append(f"{tracked}: docs/ holds markdown documents only; assets live where the baseline sends them")
            continue
        folder = "/".join(tracked.split("/")[:2])
        if f"({folder}/)" not in rows:
            problems.append(f"{tracked}: {folder}/ has no row in the AGENTS.md index; a subfolder of docs/ is a registered record folder or it does not exist")
        if folder != "docs/inherited" and not DATED_RECORD_NAME.match(tracked.rsplit("/", 1)[-1]):
            problems.append(
                f"{tracked}: a file below a docs/ subfolder is a dated record named YYYY-MM-DD-short-kebab-title.md; "
                f"a living document is a flat UPPERCASE file at the top of docs/"
            )


def check_records(problems: list[str], root: Path) -> None:
    """Names and status lines for every numbered record folder, and claim shapes."""
    for folder, status in (
        ("docs/decisions", DECISION_STATUS),
        ("docs/inherited", DECISION_STATUS),
        ("docs/claims", CLAIM_STATUS),
    ):
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
    """A record changes only on its Status line, in the working tree and in every commit since this scope arrived.

    The rule binds from the commit that brought its current scope sentence into the tree, found
    in git's own history, so an adopting project is held from its adoption forward, never
    re-litigates a past it did not write under the rule, and is never caught by a widened scope
    reaching behind its own arrival. A shallow clone cannot show that history, so it fails rather
    than quietly checking less.
    """
    if root != ROOT:
        return
    if git("rev-parse", "--is-shallow-repository") == "true":
        problems.append("the clone is shallow, so record history cannot be checked; fetch the full history")
        return
    # Every subfolder of docs/ except the arrow manifests is a record folder, so the diff is
    # read over docs/ and only files below such a folder count; living documents change freely.
    arrivals = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_inquiry.py").split()
    diffs = [("the working tree", git("diff", "HEAD", "--unified=0", "--diff-filter=M", "--", "docs"))]
    if arrivals:
        commits = [arrivals[0], *git("log", "--format=%H", f"{arrivals[0]}..HEAD", "--diff-filter=M", "--", "docs").split()]
        diffs.extend(
            (sha[:12], git("show", sha, "--format=", "--unified=0", "-M", "--diff-filter=M", "--", "docs"))
            for sha in commits
        )
    for where, diff in diffs:
        current = ""
        flagged: set[str] = set()
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                current = line[6:]
                below = current.split("docs/", 1)[1] if "docs/" in current else ""
                if "/" not in below or below.startswith("arrows/"):
                    current = ""
                continue
            if not current:
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


def section_body(text: str, heading: str) -> str:
    """The text of one section of a record, empty when the section is absent."""
    if heading not in text:
        return ""
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def check_reviews(problems: list[str], root: Path) -> None:
    """Every review pass carries its shape, names its boundary's completeness, runs or collapses each stage in writing, and names the pass it extends.

    Whether the boundary was well chosen or the reading was good stays with review; what is held
    here is that a pass claiming exhaustion ran the completeness review, that the checks never
    collapse, and that a collapsed stage names its reason.
    """
    folder = root / "docs/reviews"
    if not folder.exists():
        return
    for path in sorted(folder.glob("*.md")):
        rel = f"docs/reviews/{path.name}"
        text = path.read_text(encoding="utf-8")
        if not any(line.startswith("Date: ") for line in text.split("\n")):
            problems.append(f"{rel}: no Date line")
        for heading in REVIEW_SECTIONS:
            if heading not in text:
                problems.append(f"{rel}: section {heading!r} missing")
        completeness = COMPLETENESS.search(section_body(text, "## Boundary"))
        if completeness is None:
            problems.append(f"{rel}: the Boundary ends with a line Completeness: exhausted or Completeness: judgment")
        stages = {name: (mode, tail) for name, mode, tail in STAGE_LINE.findall(section_body(text, "## Stages"))}
        for name in REVIEW_STAGES:
            if name not in stages:
                problems.append(f"{rel}: stage {name} has no line; each stage ran or collapsed in writing")
            elif stages[name][0] == "collapsed" and len(stages[name][1].strip(" ,.")) < 3:
                problems.append(f"{rel}: stage {name} collapsed without a reason; a collapse costs one written line")
        if stages.get("Checks", ("ran", ""))[0] == "collapsed":
            problems.append(f"{rel}: the checks never collapse, because they are free")
        if completeness and completeness.group(1) == "exhausted" and stages.get("Completeness review", ("collapsed", ""))[0] != "ran":
            problems.append(f"{rel}: a pass claiming its boundary exhausted ran the completeness review; otherwise it claims judgment")
        slice_text = section_body(text, "## Slice")
        if "First pass" not in slice_text:
            prior = [t for t in LINK.findall(slice_text) if t.endswith(".md")]
            if not prior:
                problems.append(f"{rel}: the Slice names the prior pass it extends or says First pass")
            problems.extend(
                f"{rel}: extends {target}, which does not exist"
                for target in prior if not (path.parent / target.split("#", 1)[0]).exists()
            )


def prose_only(text: str) -> str:
    """The text with its code spans blanked, because a key in backticks is a mention, not a citation."""
    return CODE_SPAN.sub(" ", text)


def check_citations(problems: list[str], root: Path) -> None:
    """Every cited key resolves in the bibliography; a key inside backticks is a mention and is not read."""
    bib = root / "docs/BIBLIOGRAPHY.md"
    keys = set()
    if bib.exists():
        for line in bib.read_text(encoding="utf-8").split("\n"):
            entry = BIB_ENTRY.match(line)
            if entry:
                keys.add(entry.group(1))
    sources = [*(root / rel for rel in living_documents(root)),
               *sorted((root / "docs/claims").glob("*.md")),
               *sorted((root / "docs/decisions").glob("*.md")),
               *(sorted((root / "docs/reviews").glob("*.md")) if (root / "docs/reviews").exists() else [])]
    for path in sources:
        if not path.exists():
            continue
        for cited in CITE_KEY.findall(prose_only(path.read_text(encoding="utf-8"))):
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
    check_reviews(problems, root)
    check_citations(problems, root)
    check_arrows(problems, root)
    check_pins(problems, advice, root)
    return problems, advice


PLANTS = [
    ("docs/claims/0009-planted.md",
     "# 0009. Planted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "settled claim has no evidence"),
    ("docs/claims/0008-planted.md",
     "# 0008. Planted\n\nStatus: Refuted\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nkilled by y at arrows/planted at 0123456789ab.\n\n## Threats\n\n- None named.\n",
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


# A well-formed review pass; each review plant breaks exactly one rule of it.
REVIEW_TEMPLATE = (
    "# Planted pass\n\nDate: 2026-01-01\n\n## Slice\n\nFirst pass over the planted slice.\n\n"
    "## Boundary\n\nRead the works the question cites and nothing else.\nCompleteness: judgment\n\n"
    "## Method\n\nA scoping read of a known corpus.\n\n## Stages\n\n"
    "- Scouting: collapsed, the slice was already scouted by the question.\n"
    "- Enumeration: ran, over the cited works.\n"
    "- Checks: ran, every key resolves.\n"
    "- Completeness review: collapsed, no completeness is claimed.\n"
    "- Fold: collapsed, the ledger did not move.\n"
    "- Resolution: collapsed, no two sources conflict.\n\n"
    "## Found\n\n[planted9999].\n\n## Changed\n\nNothing in the ledger.\n\n## Left out\n\nEvery database.\n"
)
REVIEW_PLANTS = [
    ("docs/reviews/2026-01-01-planted-no-boundary.md", REVIEW_TEMPLATE.replace("## Boundary", "## Bounds"), "section '## Boundary' missing"),
    ("docs/reviews/2026-01-01-planted-exhausted.md", REVIEW_TEMPLATE.replace("Completeness: judgment", "Completeness: exhausted"), "ran the completeness review"),
    ("docs/reviews/2026-01-01-planted-checks-collapsed.md", REVIEW_TEMPLATE.replace("- Checks: ran, every key resolves.", "- Checks: collapsed, no time this pass."), "the checks never collapse"),
    ("docs/reviews/2026-01-01-planted-no-prior.md", REVIEW_TEMPLATE.replace("First pass over the planted slice.", "Extends an earlier pass."), "names the prior pass it extends or says First pass"),
    ("docs/reviews/2026-01-01-planted-no-fold.md", REVIEW_TEMPLATE.replace("- Fold: collapsed, the ledger did not move.\n", ""), "stage Fold has no line"),
    ("docs/reviews/2026-01-01-planted-bare-collapse.md", REVIEW_TEMPLATE.replace("- Resolution: collapsed, no two sources conflict.", "- Resolution: collapsed."), "collapsed without a reason"),
    ("docs/reviews/2026-01-01-planted-dead-prior.md", REVIEW_TEMPLATE.replace("First pass over the planted slice.", "Extends [an earlier pass](2025-01-01-nothing-here.md)."), "which does not exist"),
]

# Plants the tracked-tree checks can see; each is intent-to-added for one run.
TRACKED_PLANTS = [
    ("docs/legacy/OLD.md", "# Old\n", "docs/legacy/ has no row in the AGENTS.md index"),
    ("docs/legacy/GUIDE.md", "# Guide\n", "a living document is a flat UPPERCASE file at the top of docs/"),
    ("docs/inherited/0002-planted.md", "# 0002. Planted\n\nNo status line here.\n",
     "docs/inherited/0002-planted.md: no legal Status line"),
    ("docs/diagram.png", "not a document\n", "docs/ holds markdown documents only"),
    ("stray/note.txt", "nobody gave this a room\n", "stray/: exists in the tree but has no room"),
    ("ROGUE.txt", "nobody named this\n", "ROGUE.txt: sits at the root but neither the map nor the baseline names it"),
]

# The well-formed pass cites this key, planted in the bibliography for the review plants alone.
PLANTED_ENTRY = b"- **planted9999**: Planted, P. 9999. A work entered by the selftest and removed after it.\n"

# A superseded conjecture keeps Evidence None. and must PASS, or this checker
# would force evidence into an immutable record to earn a clean run; and a key
# inside backticks is a mention of the form, so a record explaining the form must PASS too.
LEGAL_PLANTS = [
    ("docs/claims/0005-planted-legal.md",
     ("# 0005. Planted legal\n\nStatus: Superseded by 0002\nDate: 2026-01-01\n\n"
      "## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n")),
    ("docs/claims/0004-planted-legal-mention.md",
     ("# 0004. Planted legal mention\n\nStatus: Conjecture\nDate: 2026-01-01\n\n"
      "## Claim\n\nA key written as `[nobody9999]` names the citation form and cites nothing.\n\n"
      "## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n")),
]


def selftest() -> int:
    """Prove each rule fires against a planted defect, then leave no trace.

    A plant builds whatever it names, an arrow, a manifest, a bibliography entry, rather than
    naming what this tree happens to carry, so the proof holds in a project built from this
    template that carries none of the demo.
    """
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
    # The manifest-currency rule judges an arrow against its manifest, so the plant builds both
    # rather than naming whatever arrow this tree happens to carry.
    arrows_dir = ROOT / "arrows"
    manifests_dir = ROOT / "docs/arrows"
    built = [folder for folder in (manifests_dir, arrows_dir) if not folder.exists()]
    planted_arrow = arrows_dir / "planted" / "README.md"
    planted_manifest = manifests_dir / "planted.md"
    planted_claim = ROOT / "docs/claims/0095-planted-unlisted.md"
    try:
        planted_arrow.parent.mkdir(parents=True, exist_ok=True)
        manifests_dir.mkdir(exist_ok=True)
        planted_arrow.write_text("# planted\n", encoding="utf-8")
        planted_manifest.write_text("# Arrow: planted\n", encoding="utf-8")
        planted_claim.write_text(
            "# 0095. Planted unlisted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n"
            "## Evidence\n\nrun at arrows/planted at 0123456789ab.\n\n## Threats\n\n- None named.\n",
            encoding="utf-8",
        )
        unlisted_problems, _ = run(ROOT)
        if not any("docs/arrows/planted.md: does not list 0095-planted-unlisted.md" in p for p in unlisted_problems):
            failures += 1
            print("WRONG: a current claim pinned to an arrow its manifest does not list raised nothing")
    finally:
        for target in (planted_claim, planted_manifest, planted_arrow):
            target.unlink(missing_ok=True)
        planted_arrow.parent.rmdir()
        for folder in built:
            folder.rmdir()
    # The review plants cite a key, so the key is planted in the bibliography for their duration
    # and the file's bytes are restored afterwards.
    bibliography = ROOT / "docs/BIBLIOGRAPHY.md"
    original_bibliography = bibliography.read_bytes() if bibliography.exists() else None
    bibliography.write_bytes((original_bibliography or b"# Bibliography\n").rstrip(b"\n") + b"\n" + PLANTED_ENTRY)
    (ROOT / "docs/reviews").mkdir(exist_ok=True)
    try:
        for rel, content, expect in REVIEW_PLANTS:
            target = ROOT / rel
            target.write_text(content, encoding="utf-8")
            try:
                review_problems, _ = run(ROOT)
                if not any(expect in p for p in review_problems):
                    failures += 1
                    print(f"WRONG: review plant {rel} did not raise {expect!r}")
            finally:
                target.unlink()
        # The well-formed pass itself must pass, or the shape would forbid the only legal record.
        target = ROOT / "docs/reviews/2026-01-01-planted-legal-pass.md"
        target.write_text(REVIEW_TEMPLATE, encoding="utf-8")
        try:
            legal_review, _ = run(ROOT)
            if any("2026-01-01-planted-legal-pass" in p for p in legal_review):
                failures += 1
                print(f"WRONG: a well-formed review pass raised {[p for p in legal_review if 'planted-legal-pass' in p][:2]}")
        finally:
            target.unlink()
    finally:
        if original_bibliography is None:
            bibliography.unlink()
        else:
            bibliography.write_bytes(original_bibliography)
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
    # A project built from this template carries the template's records in an inherited folder,
    # numbered and registered by one row, so a legal one must PASS; the plant builds the row too.
    agents_path = ROOT / "AGENTS.md"
    original_agents = agents_path.read_bytes()
    inherited = ROOT / "docs/inherited/0001-planted-inherited.md"
    inherited.parent.mkdir(exist_ok=True)
    inherited.write_text(
        "# 0001. Planted inherited\n\nStatus: Accepted\nDate: 2026-01-01\n\n"
        "## Context\n\nx.\n\n## Decision\n\nx.\n\n## Consequences\n\nx.\n",
        encoding="utf-8",
    )
    git("add", "-N", "--", "docs/inherited/0001-planted-inherited.md")
    row = b"| [docs/inherited/](docs/inherited/) | Planted: the style's records, carried whole. |\n"
    try:
        agents_path.write_bytes(original_agents.rstrip(b"\n") + b"\n\n" + row)
        inherited_problems, _ = run(ROOT)
        if any("inherited" in p for p in inherited_problems):
            failures += 1
            print(f"WRONG: a legal inherited record raised {[p for p in inherited_problems if 'inherited' in p][:2]}")
    finally:
        agents_path.write_bytes(original_agents)
        git("rm", "--cached", "-q", "--", "docs/inherited/0001-planted-inherited.md")
        inherited.unlink()
        inherited.parent.rmdir()
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
                f"## Evidence\n\nrun at arrows/planted at 0123456789ab.\n\nfigure drift: {value}\n\n## Threats\n\n- None named.\n",
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
    # The immutability rule is dated by its scope sentence, so the commit the search finds must
    # be the one that introduced that sentence: its parent must not contain it. A history without
    # the sentence yet has nothing to prove and says so.
    arrival = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_inquiry.py").split()
    if not arrival:
        print("anchor plant skipped: the immutability scope sentence has not reached history yet")
    else:
        parent = git("show", f"{arrival[0]}^:scripts/audit_inquiry.py")
        if IMMUTABILITY_SCOPE in parent:
            failures += 1
            print("WRONG: the immutability anchor is older than the commit that introduced the current scope")
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
