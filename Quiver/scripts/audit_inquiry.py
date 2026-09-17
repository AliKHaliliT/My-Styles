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
# The rulebook grows with the law it states, as the manual and the map grow with the system.
FREE_GROWING = {"AGENTS.md", "README.md", "docs/ARCHITECTURE.md", "docs/BIBLIOGRAPHY.md", "docs/UPSTREAM.md", "docs/CONVENTIONS.md"}
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
# The upstream file a project built from this template carries: one Open section, entries dated by
# heading with a kind, a pin, and four labeled parts, expiring on the same horizon as STATE.
UPSTREAM_ENTRY = re.compile(r"^### (\d{4}-\d{2}-\d{2}) (.+)$", re.MULTILINE)
UPSTREAM_KIND = re.compile(r"^Kind: (improvement|defect)$", re.MULTILINE)
UPSTREAM_PIN = re.compile(r"^Pin: [0-9a-f]{7,40}$", re.MULTILINE)
UPSTREAM_PARTS = ("**What it is", "**How the work surfaced it", "**Records checked")
UPSTREAM_WHY = ("**Why it is believed better", "**What was worked around")
UPSTREAM_ALIGNED = re.compile(r"^Aligned to .+ at (`?[0-9a-f]{7,40}`?|the host's own commit)\.?$", re.MULTILINE)
# A key is an author name closed by a year, or a standard's designation with
# its year suffixed, so digits may sit inside the name (ieee754-2019).
CITE_KEY = re.compile(r"\[([a-z][a-z0-9]*[0-9]{4}[a-z]?|[a-z][a-z0-9]*-[0-9]{4})\](?!\()")
# A key inside backticks names the form and cites nothing, so code spans are blanked before
# citations are read; the rulebook's own example of the form is the case that needs this.
CODE_SPAN = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)
BIB_ENTRY = re.compile(r"^- \*\*([a-z][a-z0-9]*[0-9]{4}[a-z]?|[a-z][a-z0-9]*-[0-9]{4})\*\*:")
PIN = re.compile(r"arrows/([a-z0-9-]+) at ([0-9a-f]{7,40})\b")
# A manifest's verification: a claim number and the commit at which its figures reproduced.
VERIFIED = re.compile(r"\b(\d{4}) at ([0-9a-f]{7,40})\b")
# Evidence observed once and never re-run declares itself on one line of the Evidence section.
RECORDED = re.compile(r"^Recorded: (.+)$", re.MULTILINE)
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
# A queued, deferred, or blocked entry that stands unchanged for two horizons is a decision
# record trying to be born, and the file cannot show it, because a date is the entry's
# last-verified stamp rather than its birthday; so the age is read from history, from the first
# commit that carried the entry's text, and like every history-reading check this one binds
# from the arrival of its own scope sentence, counting no entry's age from before it.
STATE_AGE_SCOPE = "entries of Next, Deferred, and Blocked held to two horizons of unchanged text"
STATE_TEXT = re.compile(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$")
# A record's filename stays within this many characters, because the folders it lives under are
# deep and a Windows clone has a path limit; like every history-reading check, the cap binds from
# the arrival of its own scope sentence, so a record added in a commit before that arrival is
# never judged. Before means an earlier commit, never an earlier date, because two commits on
# one day are ordered by the history and not by the calendar.
RECORD_NAME_SCOPE = "record filenames held to seventy-two characters"
NAME_CAP = 72
# A link into a numbered record folder is a citation, and a citation carries the record's title
# in its paragraph, so the sentence stands without the click and cannot drift from what it cites.
RECORD_LINK = re.compile(r"(?:decisions|inherited|claims)/(\d{4})-[a-z0-9-]+\.md$")
# A record the inherited folder gains at a re-alignment is cited by a record of the project's
# own, the re-alignment's, which says what the rule did to the tree; reading a record is not
# applying it, and a rule with no check reaches the tree only through the hand that says what it
# did with it. The check decides the citation and review decides its honesty. Like every
# history-reading check it binds from the arrival of its own scope sentence, and the folder's
# first arrival, the adoption, is exempt, because the adoption record stands for it whole.
DISPOSITION_SCOPE = "records the inherited folder gained held to a citing record of the project's own"
INHERITED_CITATION = re.compile(r"inherited/(\d{4})-[a-z0-9-]+\.md")
# An arrow carried inside its style's repository is aligned at the host's own commit, its
# inherited folder moving with every landing under the family audit, so no re-alignment gains it
# a record and the disposition check does not apply there.
HOST_OWN_COMMIT = "at the host's own commit"
# A prose paragraph that names this many references or more is an enumeration wearing prose, a
# list or a table with its rows run together; measured over the family and over a project built
# from it, everything at this count was a schema stated as prose or a set of bindings, and
# everything argued sat well below it. Whether a given paragraph is one of those stays with
# review, so the count advises and never gates.
DENSE_PARAGRAPH = 8
REFERENCE = re.compile(r"`[^`\n]+`|\[[^\]]*\]\([^)\s]+\)")
NOT_PROSE = ("#", "- ", "* ", "|", ">")


# Questions about committed history have one answer for the life of a process, because nothing
# here commits: a plant writes a file or adds it to the index and history stays as it was. So
# these subcommands are asked once and remembered, and the selftest's forty runs stop repeating
# the same walks. A question that reads the working tree or the index, diff, ls-files, status,
# is never remembered, since the plants change exactly that between runs.
HISTORY_COMMANDS = ("log", "show", "rev-list", "rev-parse", "ls-tree")
HISTORY_ANSWERS: dict[tuple[str, ...], str] = {}


def git(*args: str) -> str:
    """One git call against the repository this file lives in; answers about committed history are kept."""
    remembered = bool(args) and args[0] in HISTORY_COMMANDS
    if remembered and args in HISTORY_ANSWERS:
        return HISTORY_ANSWERS[args]
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    answer = done.stdout.strip() if done.returncode == 0 else ""
    if remembered:
        HISTORY_ANSWERS[args] = answer
    return answer


def tracked_files() -> list[str]:
    """Every tracked path, posix and relative to the root, so untracked local clutter never fires a check."""
    return [p for p in git("ls-files", "-z").split("\0") if p]


def first_commit(needle: str, path: str) -> str | None:
    """The first commit whose diff of the path carries the needle, or None."""
    found = git("log", "--reverse", "--format=%H", "-S", needle, "--", path).split("\n")[0].strip()
    return found or None


def commit_date(commit: str) -> date:
    """The committer date of one commit."""
    return date.fromisoformat(git("show", "-s", "--format=%cs", commit).strip())


def is_before(commit: str, other: str) -> bool:
    """Whether the first commit is a proper ancestor of the second, which is what before means in a history."""
    return commit != other and git("rev-list", "--count", f"{other}..{commit}").strip() == "0"


def added_commits(prefix: str) -> dict[str, str]:
    """The commit that first added each tracked file under the prefix, from one walk of history."""
    commits: dict[str, str] = {}
    current: str | None = None
    # Names in the log are relative to the repository top, while this audit may run from a folder
    # below it, so the folder prefix is stripped before the names are compared.
    top_prefix = git("rev-parse", "--show-prefix").strip()
    log = git("log", "--reverse", "--no-renames", "--diff-filter=A", "--format=@@%H", "--name-only", "--", prefix)
    for line in log.split("\n"):
        if line.startswith("@@"):
            current = line[2:].strip()
        elif line and current is not None:
            commits.setdefault(line.removeprefix(top_prefix), current)
    return commits


def check_record_names(problems: list[str], root: Path) -> None:
    """Records written after the cap arrived keep their filenames within it; carried folders are exempt."""
    docs = root / "docs"
    if root != ROOT or not docs.is_dir():
        return
    arrival = first_commit(RECORD_NAME_SCOPE, "scripts/audit_inquiry.py")
    added = added_commits("docs")
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel.count("/") < 2 or rel.startswith("docs/inherited/"):
            continue
        if len(path.name) <= NAME_CAP:
            continue
        born = added.get(rel)
        judged = born is None or (arrival is not None and not is_before(born, arrival))
        if judged:
            problems.append(
                f"{rel}: filename is {len(path.name)} characters, the cap is {NAME_CAP}; "
                "a title is short, and the folders above it are not"
            )


def aligned_at_host(root: Path) -> bool:
    """Whether the upstream file aligns this tree at the host's own commit, as an arrow carried inside its style's repository is."""
    upstream = root / "docs/UPSTREAM.md"
    return upstream.exists() and HOST_OWN_COMMIT in upstream.read_text(encoding="utf-8")


def check_dispositions(problems: list[str], root: Path) -> None:
    """Every record the inherited folder gained after adoption is cited by a record of the project's own."""
    inherited = root / "docs/inherited"
    if root != ROOT or not inherited.is_dir() or aligned_at_host(root) or not git("ls-tree", "-r", "--name-only", "HEAD", "--", "docs/inherited"):
        return
    cited: set[str] = set()
    for record in (root / "docs/decisions").glob("*.md"):
        cited.update(INHERITED_CITATION.findall(record.read_text(encoding="utf-8")))
    uncited = [p for p in sorted(inherited.glob("*.md")) if RECORD_NAME.match(p.name) and p.name[:4] not in cited]
    if not uncited:
        return
    arrival = first_commit(DISPOSITION_SCOPE, "scripts/audit_inquiry.py")
    added = added_commits("docs/inherited")
    adoption = git("log", "--reverse", "--format=%H", "--diff-filter=A", "--", "docs/inherited").split("\n")[0].strip()
    for path in uncited:
        born = added.get(f"docs/inherited/{path.name}")
        if born == adoption or (born is not None and (arrival is None or is_before(born, arrival))):
            continue
        problems.append(
            f"docs/inherited/{path.name}: gained by a re-alignment and cited by no record of this project's own;"
            " the re-alignment's record names each record the folder gained with what it bound and what changed,"
            " or that it bound nothing and why"
        )


def record_body(text: str) -> str:
    """A record's text beyond its heading and its Status line, the two lines a copy under another number changes."""
    lines = text.replace("\r\n", "\n").strip().split("\n")
    return "\n".join(line for line in lines[1:] if not line.startswith("Status: ")).strip()


def check_template_copies(problems: list[str], root: Path) -> None:
    """No record of the project's own is an inherited record's body under another number."""
    inherited = root / "docs/inherited"
    decisions = root / "docs/decisions"
    if not inherited.is_dir() or not decisions.is_dir():
        return
    bodies = {record_body(p.read_text(encoding="utf-8")): p.name for p in inherited.glob("*.md")}
    for own in sorted(decisions.glob("*.md")):
        twin = bodies.get(record_body(own.read_text(encoding="utf-8")))
        if twin is not None:
            problems.append(
                f"docs/decisions/{own.name}: is the template's record docs/inherited/{twin} under this project's number;"
                " docs/decisions/ holds the project's own decisions and nothing else, so delete it, the inherited folder carries it"
            )


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
    check_living_documents(problems, root, rows)
    check_state(problems, root)
    check_docs_below_top(problems, root, rows)


def check_living_documents(problems: list[str], root: Path, rows: str) -> None:
    """Every living document exists, stays within its budget where bounded, and has its row in the index."""
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


def check_state(problems: list[str], root: Path) -> None:
    """The STATE schema: four sections, a capped Now, and every entry dated within its horizon."""
    state = root / "STATE.md"
    if not state.exists():
        return
    text = state.read_text(encoding="utf-8")
    for section in ("## Now", "## Next", "## Deferred", "## Blocked"):
        if section not in text:
            problems.append(f"STATE.md: section {section!r} missing")
    now = text.split("## Now", 1)[-1].split("##", 1)[0]
    entries = [l for l in now.split("\n") if l.startswith("- ") and "Nothing" not in l]
    if len(entries) > NOW_CAP:
        problems.append(f"STATE.md: Now holds {len(entries)} entries, cap is {NOW_CAP}")
    binding = first_commit(STATE_AGE_SCOPE, "scripts/audit_inquiry.py") if root == ROOT else None
    check_state_entries(problems, text, binding)


def standing_days(raw: str, binding: str, today: date) -> int:
    """How long a queued entry has stood unchanged, counted from the binding commit or the entry's own, whichever is later."""
    born = first_commit(STATE_TEXT.sub("", raw).strip(), "STATE.md")
    start = None if born is None else commit_date(binding if is_before(born, binding) else born)
    return (today - start).days if start is not None else 0


def check_state_entries(problems: list[str], text: str, binding: str | None) -> None:
    """Every entry carries a date within its section's horizon, and no queued entry has stood for two of them."""
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
        if section == "Now" or binding is None:
            continue
        standing = standing_days(raw, binding, today)
        if standing > HORIZON_DAYS * 2:
            problems.append(
                f"STATE.md: entry has stood unchanged in {section} for {standing} days, two horizons; "
                f"promote it to Now, write it as a decision record, or drop it: {raw.strip()[:60]}"
            )


def check_docs_below_top(problems: list[str], root: Path, rows: str) -> None:
    """Below the top level, docs/ holds registered record folders of dated records and the manifests, nothing else.

    Everything else under docs/ is a document with a room or it does not exist. A file below
    a subdirectory is registered by its own path or by its directory's row in the index; a
    file that is not markdown has no species and no room here at all. A record folder beyond
    the numbered ones holds dated documents, registered by its own row; a living document
    belongs at the top as a flat UPPERCASE file, where the naming and budget rules can see it,
    so anything else below a subfolder fails.
    """
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
        # Numbers are unique within a folder and never compared across them; two sessions that
        # each wrote the next number merge without a textual conflict, and this is where it shows.
        advice = "recopy the folder whole from the template" if folder == "docs/inherited" else "renumber the newer record"
        numbers: dict[str, str] = {}
        for path in sorted((root / folder).glob("*.md")):
            rel = f"{folder}/{path.name}"
            if not RECORD_NAME.match(path.name):
                problems.append(f"{rel}: name breaks NNNN-kebab-title.md")
            number = path.name[:4]
            if number in numbers:
                problems.append(f"{folder}/: {numbers[number]} and {path.name} share the number {number}; {advice}")
            numbers[number] = path.name
            text = path.read_text(encoding="utf-8")
            lines = text.split("\n")
            if not any(status.match(l) for l in lines):
                problems.append(f"{rel}: no legal Status line")
            if not any(l.startswith("Date: ") for l in lines):
                problems.append(f"{rel}: no Date line")
            if folder.endswith("claims"):
                check_claim_shape(problems, rel, text, lines)


def check_claim_shape(problems: list[str], rel: str, text: str, lines: list[str]) -> None:
    """A claim carries its three sections, evidence that matches its status, and a reopening condition when refuted.

    A superseded record is exempt on both sides. Its evidence lives in its superseder,
    because immutability forbids a conjecture ever gaining evidence in place. The owner
    approved this rule after the check wrongly failed the first settled conjecture.
    """
    for section in ("## Claim", "## Evidence", "## Threats"):
        if section not in text:
            problems.append(f"{rel}: section {section!r} missing")
    body = text.split("## Evidence", 1)[-1].split("##", 1)[0].strip()
    is_conjecture = any(l == "Status: Conjecture" for l in lines)
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


def prose_paragraphs(text: str) -> list[tuple[int, str]]:
    """Every prose paragraph with the line it starts on; fences, headings, list items, table rows, and quotes are not prose."""
    paragraphs: list[tuple[int, str]] = []
    buffer: list[str] = []
    start = 0
    in_fence = False
    for number, line in enumerate(text.split("\n"), 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip() or line.lstrip().startswith(NOT_PROSE) or re.match(r"^\s*\d+\.\s", line):
            if buffer:
                paragraphs.append((start, " ".join(buffer)))
                buffer = []
            continue
        start = start if buffer else number
        buffer.append(line.strip())
    if buffer:
        paragraphs.append((start, " ".join(buffer)))
    return paragraphs


def advise_dense_paragraphs(advice: list[str], rel: str, text: str) -> None:
    """A prose paragraph naming eight or more references is advised to become a list or a table; the facts stay, the shape changes."""
    for line, paragraph in prose_paragraphs(text):
        count = len(REFERENCE.findall(paragraph))
        if count >= DENSE_PARAGRAPH:
            advice.append(
                f"{rel}:{line}: this paragraph names {count} references; a list or a table shows them, a paragraph argues, "
                "and every fact it holds survives the move"
            )


def record_title(record: Path) -> str | None:
    """The title a record's heading states, after its number, or None where the heading is not in the form."""
    first = record.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    if not first.startswith("# ") or ". " not in first:
        return None
    return first.split(". ", 1)[1].strip()


def check_record_citations(problems: list[str], rel: str, path: Path, text: str) -> None:
    """Every link to a record carries the record's title in the same paragraph, so the sentence stands without the click."""
    for paragraph in re.split(r"\n\s*\n", text):
        for target in LINK.findall(paragraph):
            record = path.parent / target.split("#", 1)[0]
            if not RECORD_LINK.search(target.split("#", 1)[0]) or not record.exists():
                continue
            title = record_title(record)
            if title is None or title in paragraph:
                continue
            line = text.count("\n", 0, text.find(f"]({target})")) + 1
            problems.append(f"{rel}:{line}: cites {record.name[:4]} without its title; a citation carries the number and the title, {title}")


def check_references(problems: list[str], root: Path) -> None:
    """Every relative link in a living document resolves, every root-anchored path it names exists, and every record cited carries its title."""
    for rel in living_documents(root):
        path = root / rel
        if not path.exists():
            continue
        check_record_citations(problems, rel, path, path.read_text(encoding="utf-8"))
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


def check_upstream(problems: list[str], root: Path) -> None:
    """The upstream file's schema and horizon, where a project carries one."""
    path = root / "docs/UPSTREAM.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if not UPSTREAM_ALIGNED.search(text):
        problems.append("docs/UPSTREAM.md: no Aligned line naming the template and the commit the project is aligned to")
    if "## Open" not in text:
        problems.append("docs/UPSTREAM.md: no ## Open section")
        return
    body = text.split("## Open", 1)[1]
    entries = list(UPSTREAM_ENTRY.finditer(body))
    if not entries and "Nothing open." not in body:
        problems.append("docs/UPSTREAM.md: Open holds entries or the words Nothing open.")
    if entries and "Nothing open." in body:
        problems.append("docs/UPSTREAM.md: says Nothing open. beside open entries")
    today = datetime.now(timezone.utc).date()
    for index, entry in enumerate(entries):
        end = entries[index + 1].start() if index + 1 < len(entries) else len(body)
        check_upstream_entry(problems, entry, body[entry.end():end], today)


def check_upstream_entry(problems: list[str], entry: re.Match[str], chunk: str, today: date) -> None:
    """One upstream entry carries its kind, its pin, its four parts, and a date within the horizon."""
    label = f"docs/UPSTREAM.md: entry {entry.group(1)} {entry.group(2)[:40]}"
    if not UPSTREAM_KIND.search(chunk):
        problems.append(f"{label}: no Kind line reading improvement or defect")
    if not UPSTREAM_PIN.search(chunk):
        problems.append(f"{label}: no Pin line naming the template commit")
    for part in UPSTREAM_PARTS:
        if part not in chunk:
            problems.append(f"{label}: part {part}** missing")
    if not any(why in chunk for why in UPSTREAM_WHY):
        problems.append(f"{label}: neither Why it is believed better nor What was worked around")
    if (today - date.fromisoformat(entry.group(1))).days > HORIZON_DAYS:
        problems.append(
            f"{label}: past the {HORIZON_DAYS}-day horizon; re-verify against the template and re-date,"
            " or make it the project's own decision and delete it"
        )


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


WORKING_TREE_DIRS = (".worktrees/", ".claude/worktrees/")


def check_ignored_working_trees(problems: list[str], root: Path) -> None:
    """The ignore file names every directory a second working tree may occupy."""
    ignore = root / ".gitignore"
    lines = [line.strip() for line in ignore.read_text(encoding="utf-8").splitlines()] if ignore.exists() else []
    missing = [directory for directory in WORKING_TREE_DIRS if directory not in lines]
    if missing:
        problems.append(
            ".gitignore: a second working tree's directory is ignored before it is created;"
            f" the Working trees section names {' and '.join(WORKING_TREE_DIRS)}, missing {', '.join(missing)}"
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
    for where, diff in record_diffs():
        flag_illegal_edits(problems, where, diff)


def record_diffs() -> list[tuple[str, str]]:
    """The diff of docs/ in the working tree and in every commit since the immutability scope arrived.

    Every subfolder of docs/ except the arrow manifests is a record folder, so the diff is
    read over docs/ and only files below such a folder count; living documents change freely.
    """
    arrivals = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_inquiry.py").split()
    diffs = [("the working tree", git("diff", "HEAD", "--unified=0", "--diff-filter=M", "--", "docs"))]
    if arrivals:
        diffs.append((arrivals[0][:12], git("show", arrivals[0], "--format=", "--unified=0", "-M", "--diff-filter=M", "--", "docs")))
        # One walk prints every later commit's patch behind its own marker line, instead of one
        # process per commit, so the cost stays flat as the history grows; a merge shows what its
        # resolution changed, as show does.
        log = git("log", "-p", "--cc", "--format=%x01%H", "--unified=0", "-M", "--diff-filter=M", f"{arrivals[0]}..HEAD", "--", "docs")
        for chunk in log.split("\x01")[1:]:
            sha, _, patch = chunk.partition("\n")
            diffs.append((sha.strip()[:12], patch))
    return diffs


def flag_illegal_edits(problems: list[str], where: str, diff: str) -> None:
    """Every record the diff changes beyond its Status line, reported once each; manifests are living and pass."""
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
        check_review_stages(problems, rel, section_body(text, "## Stages"), completeness)
        check_review_slice(problems, rel, path, section_body(text, "## Slice"))


def check_review_stages(problems: list[str], rel: str, stages_text: str, completeness: re.Match[str] | None) -> None:
    """Every stage ran or collapsed in writing, the checks never collapse, and exhaustion ran the completeness review."""
    stages = {name: (mode, tail) for name, mode, tail in STAGE_LINE.findall(stages_text)}
    for name in REVIEW_STAGES:
        if name not in stages:
            problems.append(f"{rel}: stage {name} has no line; each stage ran or collapsed in writing")
        elif stages[name][0] == "collapsed" and len(stages[name][1].strip(" ,.")) < 3:
            problems.append(f"{rel}: stage {name} collapsed without a reason; a collapse costs one written line")
    if stages.get("Checks", ("ran", ""))[0] == "collapsed":
        problems.append(f"{rel}: the checks never collapse, because they are free")
    if completeness and completeness.group(1) == "exhausted" and stages.get("Completeness review", ("collapsed", ""))[0] != "ran":
        problems.append(f"{rel}: a pass claiming its boundary exhausted ran the completeness review; otherwise it claims judgment")


def check_review_slice(problems: list[str], rel: str, path: Path, slice_text: str) -> None:
    """The Slice names the prior pass it extends, and that pass exists, or it says First pass."""
    if "First pass" in slice_text:
        return
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
    for name in sorted(arrows & manifests):
        check_manifest_currency(problems, root, name)


def check_manifest_currency(problems: list[str], root: Path, name: str) -> None:
    """A manifest names exactly the current claims pinned to its arrow and verifies only those.

    A manifest is living, so the claims it says rest on the arrow are the current ones: every
    claim still standing that pins the arrow is linked, no superseded claim is, and every
    verification it records names a claim that is current here.
    """
    manifest = (root / "docs/arrows" / f"{name}.md").read_text(encoding="utf-8")
    current: set[str] = set()
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
        if not superseded and not any(l.startswith("Status: Stale") for l in text.split("\n")):
            current.add(path.name[:4])
    for number in sorted(verifications(root, name)):
        if number not in current:
            problems.append(f"docs/arrows/{name}.md: verifies {number}, which is not a current claim pinned to this arrow")


# The paths inside an arrow that can change what a run produces: the code, the
# suites, and the project file that selects dependencies and warning behavior.
# Documentation and workflow bytes carried inside an arrow execute nothing
# during an experiment, so their movement can move no number and never advises.
EVIDENCE_PATHS = ("src", "tests", "pyproject.toml")


def verifications(root: Path, arrow: str) -> dict[str, str]:
    """The latest verification pin per claim number that the arrow's manifest records."""
    manifest = root / "docs/arrows" / f"{arrow}.md"
    found: dict[str, str] = {}
    if not manifest.exists():
        return found
    for line in manifest.read_text(encoding="utf-8").split("\n"):
        if line.startswith("- **Verified**:"):
            for number, pin in VERIFIED.findall(line):
                found[number] = pin
    return found


def check_pins(problems: list[str], advice: list[str], root: Path) -> None:
    """Pins exist in history; movement past a pin, or past its latest verification, is advice.

    A recorded observation is never advised, because no command's output could have changed;
    what must hold for it is that everything it says it preserved is still in the tree.
    """
    for path in sorted((root / "docs/claims").glob("*.md")):
        rel = f"docs/claims/{path.name}"
        text = path.read_text(encoding="utf-8")
        number = path.name[:4]
        # A claim whose status already says it is not current, Stale or Superseded,
        # leaves the movement advisory nothing to prompt, so only claims still
        # standing as current are advised. The pin must be a real commit either
        # way, because a record's evidence never gets to point at nothing.
        resting = any(
            l.startswith(("Status: Stale", "Status: Superseded by")) for l in text.split("\n")
        )
        recorded = RECORDED.search(text)
        if recorded:
            check_recorded(problems, rel, recorded.group(1), root)
        for arrow, pin in PIN.findall(text):
            if not git("rev-parse", "--verify", f"{pin}^{{commit}}"):
                problems.append(f"{rel}: pin {pin} is not a commit in this history")
                continue
            if resting or recorded:
                continue
            base, basis = movement_base(problems, root, arrow, number, pin)
            spec = [f"arrows/{arrow}/{part}" for part in EVIDENCE_PATHS]
            moved = git("log", "--oneline", f"{base}..HEAD", "--", *spec)
            if moved:
                advice.append(
                    f"{rel}: arrows/{arrow} evidence paths moved past {basis} {base[:12]}"
                    f" ({len(moved.splitlines())} commit(s)); re-verify it in the manifest if the figures"
                    " reproduce, supersede it if they do not, or flip it Stale"
                )


def check_recorded(problems: list[str], rel: str, recorded: str, root: Path) -> None:
    """A recorded observation names what it preserved, by a path that exists, or says nothing preserved."""
    named = [t for t in PATH_TOKEN.findall(recorded) if claims_to_be_path(t, root)]
    if not named and "nothing preserved" not in recorded:
        problems.append(
            f"{rel}: recorded evidence names nothing preserved; name the artefact by path or say nothing preserved"
        )
    for token in named:
        if not (root / token.lstrip("./")).exists():
            problems.append(f"{rel}: recorded evidence names `{token}`, which does not exist")


def movement_base(problems: list[str], root: Path, arrow: str, number: str, pin: str) -> tuple[str, str]:
    """The commit movement is measured from, the claim's pin or a legal later verification in the arrow's manifest.

    A verification in the arrow's manifest moves the point the movement is measured from,
    while the claim keeps the pin that produced its figures. It must be a commit this history
    holds and no older than that pin, or it is a verdict and the pin stays the base.
    """
    verified = verifications(root, arrow).get(number)
    if not verified:
        return pin, "pin"
    if not git("rev-parse", "--verify", f"{verified}^{{commit}}"):
        problems.append(
            f"docs/arrows/{arrow}.md: verifies {number} at {verified}, which is not a commit in this history"
        )
        return pin, "pin"
    if git("rev-list", "--count", f"{verified}..{pin}") != "0":
        problems.append(
            f"docs/arrows/{arrow}.md: verifies {number} at {verified[:12]}, which is older than the claim's pin {pin[:12]}"
        )
        return pin, "pin"
    return verified, "verification"


# What a check needs before it can run. A check whose need is absent is reported as not run,
# with the need named, so a clean verdict never hides a check the tree gave nothing to check.
CHECK_NEEDS = (
    ("check_state", "STATE.md"),
    ("check_upstream", "docs/UPSTREAM.md"),
    ("check_dispositions", "docs/inherited"),
    ("check_template_copies", "docs/inherited"),
    ("check_reviews", "docs/reviews"),
    ("check_arrows", "docs/arrows"),
    ("check_pins", "docs/claims"),
)


def unrun_checks(root: Path) -> list[str]:
    """Every check the tree gave nothing to run, each named with what it needs."""
    unrun = [f"{name} did not run: {need} is absent from this tree" for name, need in CHECK_NEEDS if not (root / need).exists()]
    if (root / "docs/inherited").exists() and aligned_at_host(root):
        unrun.append(
            "check_dispositions did not run: docs/UPSTREAM.md aligns this arrow at the host's own commit,"
            " so the family audit holds its inherited folder and no re-alignment gains it a record"
        )
    return unrun


def run(root: Path) -> tuple[list[str], list[str]]:
    """Every decided problem and every piece of advice for one tree."""
    problems: list[str] = []
    advice: list[str] = []
    for rel in living_documents(root):
        if (root / rel).exists():
            advise_dense_paragraphs(advice, rel, (root / rel).read_text(encoding="utf-8"))
    check_living(problems, root)
    check_references(problems, root)
    check_rooms(problems, root)
    check_ignored_working_trees(problems, root)
    check_upstream(problems, root)
    check_record_names(problems, root)
    check_records(problems, root)
    check_dispositions(problems, root)
    check_template_copies(problems, root)
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
    ("docs/claims/0093-planted-with-a-title-so-long-that-it-runs-past-the-seventy-two-character-cap.md",
     "# 0093. Planted\n\nStatus: Conjecture\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
     "the cap is 72"),
    ("docs/claims/0092-planted-recorded-missing.md",
     ("# 0092. Planted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\n"
      "Recorded: one paid run, preserved as `docs/ghost-artefact.json`.\n\nrun at arrows/planted at 0123456789ab.\n\n"
      "## Threats\n\n- None named.\n"),
     "recorded evidence names `docs/ghost-artefact.json`, which does not exist"),
    ("docs/claims/0091-planted-recorded-bare.md",
     ("# 0091. Planted\n\nStatus: Supported\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n## Evidence\n\n"
      "Recorded: one paid run.\n\nrun at arrows/planted at 0123456789ab.\n\n## Threats\n\n- None named.\n"),
     "recorded evidence names nothing preserved"),
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
# Their numbers sit above any a young project's ledger reaches, so a legal plant never shares
# a number with a real claim and fails the check written for two sessions.
LEGAL_PLANTS = [
    ("docs/claims/0086-planted-legal.md",
     ("# 0086. Planted legal\n\nStatus: Superseded by 0002\nDate: 2026-01-01\n\n"
      "## Claim\n\nx.\n\n## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n")),
    ("docs/claims/0085-planted-legal-mention.md",
     ("# 0085. Planted legal mention\n\nStatus: Conjecture\nDate: 2026-01-01\n\n"
      "## Claim\n\nA key written as `[nobody9999]` names the citation form and cites nothing.\n\n"
      "## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n")),
]


# The claim body the advisory plants share; status and evidence vary per plant.
ADVISORY_BODY = (
    "# {num}. Planted advisory\n\nStatus: {status}\nDate: 2026-01-01\n\n"
    "## Claim\n\nx.\n\n## Evidence\n\n{evidence}\n\n## Threats\n\n- None named.\n"
)


def prove_single_plants() -> int:
    """Each single-file plant raises the finding it was written to raise."""
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
    return failures


def prove_legal_plants() -> int:
    """Each legal plant passes, or the checker would forbid a record the rulebook allows."""
    failures = 0
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
    return failures


def prove_unlisted_claim() -> int:
    """A current claim pinned to an arrow its manifest does not list is reported.

    The manifest-currency rule judges an arrow against its manifest, so the plant builds both
    rather than naming whatever arrow this tree happens to carry.
    """
    failures = 0
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
    return failures


def prove_review_plants() -> int:
    """Each review plant raises its finding and the well-formed pass raises nothing.

    The review plants cite a key, so the key is planted in the bibliography for their duration
    and the file's bytes are restored afterwards.
    """
    failures = 0
    bibliography = ROOT / "docs/BIBLIOGRAPHY.md"
    original_bibliography = bibliography.read_bytes() if bibliography.exists() else None
    bibliography.write_bytes((original_bibliography or b"# Bibliography\n").rstrip(b"\n") + b"\n" + PLANTED_ENTRY)
    reviews = ROOT / "docs/reviews"
    reviews_existed = reviews.exists()
    reviews.mkdir(exist_ok=True)
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
        if not reviews_existed and not any(reviews.iterdir()):
            reviews.rmdir()
    return failures


def prove_movement() -> int:
    """The movement advisory fires for a current claim past its pin and stays quiet for a resting one."""
    mover = moved_evidence_pin()
    if mover is None:
        print("advisory plants skipped: no arrow's evidence paths have moved in this history")
        return 0
    failures = 0
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
                ADVISORY_BODY.format(num=num, status=status, evidence=evidence), encoding="utf-8"
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
    return failures + prove_verifications(arrow_name, old_pin, pinned)


def prove_verifications(arrow_name: str, old_pin: str, pinned: str) -> int:
    """A legal verification silences the advisory, a recorded observation is never advised, and an illegal verification is a verdict.

    A verification in the arrow's manifest answers a movement whose figures reproduced, so
    it must silence the advisory; a recorded observation is never advised; a verification
    at a commit history lacks, or older than the pin, or of a claim that is not current,
    is a verdict. The manifest's bytes are restored afterwards.
    """
    failures = 0
    manifest_path = ROOT / "docs/arrows" / f"{arrow_name}.md"
    original_manifest = manifest_path.read_bytes()
    head = git("rev-parse", "HEAD")
    older = git("rev-parse", f"{old_pin}^")
    verified_claim = ROOT / "docs/claims/0089-planted-verified.md"
    recorded_claim = ROOT / "docs/claims/0088-planted-recorded.md"
    try:
        verified_claim.write_text(ADVISORY_BODY.format(num="0089", status="Supported", evidence=pinned), encoding="utf-8")
        recorded_claim.write_text(
            ADVISORY_BODY.format(
                num="0088",
                status="Supported",
                evidence=f"Recorded: one paid run, preserved as `docs/QUESTION.md`.\n\n{pinned}",
            ),
            encoding="utf-8",
        )
        listing = "\n- Planted: 0088-planted-recorded.md and 0089-planted-verified.md rest here for the selftest.\n"
        manifest_path.write_bytes(original_manifest.rstrip(b"\n") + f"{listing}- **Verified**: 0089 at {head}.\n".encode())
        verified_problems, verified_advice = run(ROOT)
        if any("0089" in a for a in verified_advice):
            failures += 1
            print("WRONG: a claim verified in its manifest at HEAD still raised the movement advisory")
        if any("0088" in a for a in verified_advice):
            failures += 1
            print("WRONG: a recorded observation raised the movement advisory")
        legal_noise = [p for p in verified_problems if "0089" in p or "0088" in p]
        if legal_noise:
            failures += 1
            print(f"WRONG: a legal verification or recorded claim raised {legal_noise[:2]}")
        bad_lines = [
            ("- **Verified**: 0089 at 0123456789ab.\n", "which is not a commit in this history"),
            (f"- **Verified**: 0087 at {head}.\n", "verifies 0087, which is not a current claim pinned to this arrow"),
        ]
        if older:
            bad_lines.append((f"- **Verified**: 0089 at {older}.\n", "which is older than the claim's pin"))
        else:
            print("older-verification plant skipped: the first evidence commit has no parent")
        for line, expect in bad_lines:
            manifest_path.write_bytes(original_manifest.rstrip(b"\n") + (listing + line).encode())
            bad_problems, _ = run(ROOT)
            if not any(expect in p for p in bad_problems):
                failures += 1
                print(f"WRONG: manifest line {line.strip()!r} did not raise {expect!r}")
    finally:
        manifest_path.write_bytes(original_manifest)
        verified_claim.unlink(missing_ok=True)
        recorded_claim.unlink(missing_ok=True)
    return failures


def prove_quiet_move() -> int:
    """A move in an arrow's non-evidence bytes alone raises no movement advisory."""
    quiet_mover = docs_only_moved_pin()
    if quiet_mover is None:
        print("docs-only advisory plant skipped: no arrow has moved in non-evidence bytes alone")
        return 0
    failures = 0
    arrow_name, quiet_pin = quiet_mover
    rel = "docs/claims/0096-planted-quiet.md"
    target = ROOT / rel
    target.write_text(
        ADVISORY_BODY.format(
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
    return failures


def prove_tracked_plants() -> int:
    """Each plant the tracked-tree checks read raises its finding.

    Checks that read the tracked tree need a plant git can see, so these are added with
    intent-to-add and removed from the index again; nothing reaches a commit.
    """
    failures = 0
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
    return failures


def prove_inherited_record() -> int:
    """A legal inherited record, in a registered inherited folder, passes.

    A project built from this template carries the template's records in an inherited folder,
    numbered and registered by one row, so a legal one must PASS. In such a project the folder
    is full, the row exists, and the low numbers are taken, so the plant builds only what the
    tree lacks, takes the lowest free number, and removes only what it built.
    """
    failures = 0
    agents_path = ROOT / "AGENTS.md"
    original_agents = agents_path.read_bytes()
    inherited_dir = ROOT / "docs/inherited"
    inherited_existed = inherited_dir.exists()
    inherited_dir.mkdir(exist_ok=True)
    taken = {p.name[:4] for p in inherited_dir.glob("*.md")}
    free = next(f"{n:04d}" for n in range(1, 10000) if f"{n:04d}" not in taken)
    inherited_rel = f"docs/inherited/{free}-planted-inherited.md"
    inherited = ROOT / inherited_rel
    inherited.write_text(
        f"# {free}. Planted inherited\n\nStatus: Accepted\nDate: 2026-01-01\n\n"
        "## Context\n\nx.\n\n## Decision\n\nx.\n\n## Consequences\n\nx.\n",
        encoding="utf-8",
    )
    git("add", "-N", "--", inherited_rel)
    row = b"| [docs/inherited/](docs/inherited/) | Planted: the style's records, carried whole. |\n"
    try:
        if "(docs/inherited/)" not in index_rows(original_agents.decode("utf-8")):
            agents_path.write_bytes(original_agents.rstrip(b"\n") + b"\n\n" + row)
        # The disposition check reads this plant as a record gained by a re-alignment, which its
        # own proof plants a citing record for; here the plant proves the folder's legality alone.
        inherited_problems = [p for p in run(ROOT)[0] if "cited by no record" not in p]
        if any("inherited" in p for p in inherited_problems):
            failures += 1
            print(f"WRONG: a legal inherited record raised {[p for p in inherited_problems if 'inherited' in p][:2]}")
    finally:
        agents_path.write_bytes(original_agents)
        git("rm", "--cached", "-q", "--", inherited_rel)
        inherited.unlink()
        if not inherited_existed:
            inherited_dir.rmdir()
    return failures


def prove_upstream_plants() -> int:
    """A legal UPSTREAM.md passes and each rule of its schema fires.

    A project built from this template carries an UPSTREAM.md of the same kind as STATE.md, so a
    legal one must PASS and each rule of its schema must fire. The project's own file and row
    are kept and written back, because the plant borrows the path rather than owning it.
    """
    failures = 0
    agents_path = ROOT / "AGENTS.md"
    original_agents = agents_path.read_bytes()
    upstream = ROOT / "docs/UPSTREAM.md"
    original_upstream = upstream.read_bytes() if upstream.exists() else None
    upstream_row = b"| [docs/UPSTREAM.md](docs/UPSTREAM.md) | Planted: what this project has for its style. |\n"
    head_text = "# Upstream\n\nAligned to Planted at 0123456789ab.\n\nEvery entry is a lead, not a verdict.\n\n## Open\n\n"
    today_stamp = datetime.now(timezone.utc).date().isoformat()
    parts = (
        "**What it is.** x.\n\n**How the work surfaced it.** x.\n\n"
        "**Why it is believed better.** x.\n\n**Records checked.** None.\n"
    )
    upstream_plants: list[tuple[str, str | None]] = [
        (head_text + "Nothing open.\n", None),
        ("# Upstream\n\nEvery entry is a lead, not a verdict.\n\n## Open\n\nNothing open.\n", "no Aligned line"),
        (head_text + f"### {today_stamp} Planted entry\n\nKind: defect\nPin: 0123456789ab\n\n" + parts, None),
        (head_text + "### 2026-01-01 Planted entry\n\nKind: defect\nPin: 0123456789ab\n\n" + parts, "past the 90-day horizon"),
        (head_text + f"### {today_stamp} Planted entry\n\nPin: 0123456789ab\n\n" + parts, "no Kind line"),
        (head_text + f"Nothing open.\n\n### {today_stamp} Planted entry\n\nKind: defect\nPin: 0123456789ab\n\n" + parts, "beside open entries"),
    ]
    try:
        if "(docs/UPSTREAM.md)" not in index_rows(original_agents.decode("utf-8")):
            agents_path.write_bytes(original_agents.rstrip(b"\n") + b"\n\n" + upstream_row)
        for upstream_text, upstream_expect in upstream_plants:
            upstream.write_text(upstream_text, encoding="utf-8")
            upstream_problems, _ = run(ROOT)
            hits = [p for p in upstream_problems if "UPSTREAM" in p]
            if upstream_expect is None and hits:
                failures += 1
                print(f"WRONG: a legal UPSTREAM.md raised {hits[:2]}")
            if upstream_expect is not None and not any(upstream_expect in p for p in hits):
                failures += 1
                print(f"WRONG: an UPSTREAM.md plant did not raise {upstream_expect!r}")
    finally:
        agents_path.write_bytes(original_agents)
        if original_upstream is None:
            upstream.unlink(missing_ok=True)
        else:
            upstream.write_bytes(original_upstream)
    return failures


def prove_figure_pair() -> int:
    """Two claims quoting one figure at one pin with different values are reported."""
    failures = 0
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
    return failures


def prove_citation_plant() -> int:
    """A record cited without its title is reported, and the same citation with the title passes."""
    claim = ROOT / "docs/claims/0089-planted-cited.md"
    cited = ROOT / "docs/PLANTED.md"
    claim.write_text(
        "# 0089. Planted cited claim\n\nStatus: Conjecture\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n"
        "## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
        encoding="utf-8",
    )
    failures = 0
    try:
        cited.write_text("# Planted\n\nSee [claim 0089](claims/0089-planted-cited.md) in passing.\n", encoding="utf-8")
        problems, _ = run(ROOT)
        if not any("cites 0089 without its title" in p for p in problems):
            failures += 1
            print("WRONG: a claim cited without its title raised nothing")
        cited.write_text("# Planted\n\nSee [claim 0089, Planted cited claim](claims/0089-planted-cited.md) in passing.\n", encoding="utf-8")
        titled, _ = run(ROOT)
        if any("without its title" in p for p in titled):
            failures += 1
            print("WRONG: a citation carrying the claim's title was reported as bare")
    finally:
        cited.unlink(missing_ok=True)
        claim.unlink(missing_ok=True)
    return failures


def prove_dense_plant() -> int:
    """A prose paragraph naming eight references is advised, and the same eight names as a list are not."""
    names = [f"`planted_{n}`" for n in range(DENSE_PARAGRAPH)]
    planted = ROOT / "docs/PLANTED.md"
    failures = 0
    # The tree may carry dense paragraphs of its own, so the plant is judged by what it adds.
    before = len(run(ROOT)[1])
    try:
        planted.write_text(f"# Planted\n\nThe planted paragraph names {', '.join(names)} in one breath.\n", encoding="utf-8")
        added = [a for a in run(ROOT)[1] if f"names {DENSE_PARAGRAPH} references" in a and "docs/PLANTED.md" in a]
        if len(run(ROOT)[1]) != before + 1 or not added:
            failures += 1
            print("WRONG: a prose paragraph naming eight references raised no advice of its own")
        planted.write_text("# Planted\n\n" + "".join(f"- {name}\n" for name in names), encoding="utf-8")
        if len(run(ROOT)[1]) != before:
            failures += 1
            print("WRONG: a list of eight names was advised as a dense paragraph")
    finally:
        planted.unlink(missing_ok=True)
    return failures


def prove_duplicate_numbers() -> int:
    """Two records sharing one number in a folder are reported, naming both."""
    twins = [ROOT / "docs/claims/0090-planted-twin-a.md", ROOT / "docs/claims/0090-planted-twin-b.md"]
    try:
        for twin in twins:
            twin.write_text(
                f"# 0090. {twin.stem[5:]}\n\nStatus: Conjecture\nDate: 2026-01-01\n\n## Claim\n\nx.\n\n"
                "## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
                encoding="utf-8",
            )
        twin_problems, _ = run(ROOT)
        if not any("share the number 0090" in p for p in twin_problems):
            print("WRONG: two claims sharing the number 0090 raised nothing")
            return 1
    finally:
        for twin in twins:
            twin.unlink(missing_ok=True)
    return 0


def prove_immutability() -> int:
    """A body edit to an accepted record fails and a Status flip alone passes.

    Immutability is a fact about a record's history, so this is the one plant that cannot
    build its subject; it selects the lowest-numbered accepted record of the project's own by
    that property, never by a number written here, because a project that kept its numbers
    after the inherited ones has no 0001.
    """
    record = next(
        (
            p for p in sorted((ROOT / "docs/decisions").glob("*.md"))
            if "\nStatus: Accepted\n" in p.read_text(encoding="utf-8")
        ),
        None,
    )
    if record is None:
        print("immutability plants skipped: no accepted record of this project's own to plant on")
        return 0
    failures = 0
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
    return failures


def prove_queue_age() -> int:
    """A queued entry written today passes; the firing case needs history this tree may lack.

    A queued entry written today has no history to age it, so it must PASS; an entry that has
    stood for two horizons cannot be planted without commits, so the firing case runs only where
    this tree carries one and says so otherwise.
    """
    failures = 0
    state_path = ROOT / "STATE.md"
    original_state = state_path.read_bytes()
    state_text = original_state.decode("utf-8").replace("\r\n", "\n")
    fresh = state_text.replace(
        "## Next\n\n- Nothing queued.\n",
        f"## Next\n\n- Planted queued work, written today ({datetime.now(timezone.utc).date().isoformat()}).\n",
        1,
    )
    if fresh == state_text:
        print("queue age plant skipped: Next is not empty in this tree")
    else:
        try:
            state_path.write_bytes(fresh.encode("utf-8"))
            fresh_problems, _ = run(ROOT)
            if any("stood unchanged" in p for p in fresh_problems):
                failures += 1
                print("WRONG: a queued entry written today was reported as standing for two horizons")
        finally:
            state_path.write_bytes(original_state)
    print("queue age firing case skipped: no queued entry in this tree has two horizons of history")
    return failures


def free_number(folder: Path, start: int) -> str:
    """The lowest record number from the start that no record in the folder uses, for a plant that must not collide."""
    taken = {p.name[:4] for p in folder.glob("*.md")}
    return next(f"{n:04d}" for n in range(start, 10000) if f"{n:04d}" not in taken)


def prove_template_copy() -> int:
    """A record of the project's own whose body is an inherited record's is reported, whatever its number and status."""
    decisions = ROOT / "docs/decisions"
    inherited_dir = ROOT / "docs/inherited"
    existed = inherited_dir.exists()
    inherited_dir.mkdir(exist_ok=True)
    free = free_number(inherited_dir, 1)
    own = free_number(decisions, 900)
    body = "\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\nPlanted twice.\n"
    template = inherited_dir / f"{free}-planted-template.md"
    copy = decisions / f"{own}-planted-template.md"
    try:
        template.write_text(f"# {free}. Planted template" + body, encoding="utf-8")
        copy.write_text(f"# {own}. Planted template" + body.replace("Status: Accepted", "Status: Superseded by 0999"), encoding="utf-8")
        if any(f"is the template's record docs/inherited/{template.name}" in p for p in run(ROOT)[0]):
            return 0
        print("WRONG: a record of this project's own carrying an inherited record's body raised nothing")
        return 1
    finally:
        copy.unlink(missing_ok=True)
        template.unlink(missing_ok=True)
        if not existed and not any(inherited_dir.iterdir()):
            inherited_dir.rmdir()


def prove_disposition() -> int:
    """A record the inherited folder gains with no citing record fails, and the same record cited passes.

    The firing case needs a folder that already stood in history, so it runs where the tree carries
    one, the rehearsal's child among them, and is named as skipped in the template, whose folder the
    plant builds, and in an arrow aligned at the host's own commit, which gains nothing by re-alignment.
    """
    failures = 0
    decisions = ROOT / "docs/decisions"
    inherited_dir = ROOT / "docs/inherited"
    existed = inherited_dir.exists()
    inherited_dir.mkdir(exist_ok=True)
    free = free_number(inherited_dir, 1)
    own = free_number(decisions, 900)
    gained = inherited_dir / f"{free}-planted-gained.md"
    citing = decisions / f"{own}-planted-disposition.md"
    try:
        gained.write_text(f"# {free}. Planted gained\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\nx.\n", encoding="utf-8")
        if not existed:
            print("disposition firing case skipped: this tree has no inherited folder that stood in history")
        elif aligned_at_host(ROOT):
            print("disposition firing case skipped: this arrow is aligned at the host's own commit and gains nothing by re-alignment")
        elif not any("cited by no record of this project's own" in p for p in run(ROOT)[0]):
            failures += 1
            print("WRONG: a gained record with no citing record raised nothing")
        citing.write_text(
            f"# {own}. Planted disposition\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\n"
            f"[Inherited {free}, Planted gained](../inherited/{gained.name}) bound nothing here.\n",
            encoding="utf-8",
        )
        if any("cited by no record" in p for p in run(ROOT)[0]):
            failures += 1
            print("WRONG: a gained record cited by a record of this project's own was reported as uncited")
    finally:
        citing.unlink(missing_ok=True)
        gained.unlink(missing_ok=True)
        if not existed and not any(inherited_dir.iterdir()):
            inherited_dir.rmdir()
    return failures


def prove_anchors() -> int:
    """Each history-reading rule's scope sentence is dated by the commit that introduced it.

    The rule is dated by its scope sentence, so the commit the search finds must be the one
    that introduced that sentence: its parent must not contain it. A history without the
    sentence yet has nothing to prove and says so.
    """
    failures = 0
    name_arrival = git("log", "--reverse", "--format=%H", "-S", RECORD_NAME_SCOPE, "--", "scripts/audit_inquiry.py").split()
    if name_arrival and RECORD_NAME_SCOPE in git("show", f"{name_arrival[0]}^:scripts/audit_inquiry.py"):
        failures += 1
        print("WRONG: the filename cap anchor is older than the commit that introduced the current scope")
    age_arrival = git("log", "--reverse", "--format=%H", "-S", STATE_AGE_SCOPE, "--", "scripts/audit_inquiry.py").split()
    if age_arrival and STATE_AGE_SCOPE in git("show", f"{age_arrival[0]}^:scripts/audit_inquiry.py"):
        failures += 1
        print("WRONG: the queue age anchor is older than the commit that introduced the current scope")
    disposition_arrival = git("log", "--reverse", "--format=%H", "-S", DISPOSITION_SCOPE, "--", "scripts/audit_inquiry.py").split()
    if disposition_arrival and DISPOSITION_SCOPE in git("show", f"{disposition_arrival[0]}^:scripts/audit_inquiry.py"):
        failures += 1
        print("WRONG: the disposition anchor is older than the commit that introduced the current scope")
    arrival = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_inquiry.py").split()
    if not arrival:
        print("anchor plant skipped: the immutability scope sentence has not reached history yet")
    elif IMMUTABILITY_SCOPE in git("show", f"{arrival[0]}^:scripts/audit_inquiry.py"):
        failures += 1
        print("WRONG: the immutability anchor is older than the commit that introduced the current scope")
    return failures


def prove_empty_tree() -> int:
    """An empty tree raises the missing-document problem rather than passing for lack of material."""
    with tempfile.TemporaryDirectory() as scratch:
        empty, _ = run(Path(scratch))
        if not any("missing living document" in p for p in empty):
            print("WRONG: an empty tree raised no missing-document problem")
            return 1
    return 0


def prove_ignore_plant() -> int:
    """Dropping the working-tree lines from the ignore file raises the finding, and the bytes come back."""
    ignore = ROOT / ".gitignore"
    if not ignore.exists():
        print("ignore plant skipped: no .gitignore in this tree")
        return 0
    original = ignore.read_bytes()
    kept = [line for line in original.decode("utf-8").splitlines() if line.strip() not in WORKING_TREE_DIRS]
    ignore.write_text("\n".join(kept) + "\n", encoding="utf-8")
    try:
        problems, _ = run(ROOT)
        if any("Working trees section" in p for p in problems):
            return 0
        print("WRONG: ignore plant did not raise the Working trees finding")
        return 1
    finally:
        ignore.write_bytes(original)


def prove_unrun_report() -> int:
    """Hiding a check's need names the check as not run, and the file comes back."""
    state = ROOT / "STATE.md"
    if not state.exists():
        print("unrun plant skipped: no STATE.md in this tree")
        return 0
    if any("check_state did not run" in line for line in unrun_checks(ROOT)):
        print("WRONG: check_state was reported as not run while STATE.md is present")
        return 1
    original = state.read_bytes()
    state.unlink()
    try:
        if any("check_state did not run" in line for line in unrun_checks(ROOT)):
            return 0
        print("WRONG: hiding STATE.md did not report check_state as not run")
        return 1
    finally:
        state.write_bytes(original)


def selftest() -> int:
    """Prove each rule fires against a planted defect, then leave no trace.

    A plant builds whatever it names, an arrow, a manifest, a bibliography entry, rather than
    naming what this tree happens to carry, so the proof holds in a project built from this
    template that carries none of the demo.
    """
    # A plant proves nothing in a tree that already fails, so the tree is checked first and the
    # command stops with the audit's own findings rather than counting every legal plant as a
    # broken rule.
    baseline, _ = run(ROOT)
    if baseline:
        print("the unplanted tree is not clean, so nothing can be proven until the audit passes:")
        for p in baseline[:5]:
            print(f"  {p}")
        return 1
    # Plants write into record folders a project may not have yet, a fresh inquiry among them, so
    # the folders the plants need are built here and removed again once every plant is gone.
    built_folders = [ROOT / rel for rel in ("docs/claims", "docs/arrows", "docs/reviews") if not (ROOT / rel).exists()]
    for folder in built_folders:
        folder.mkdir()
    proofs = (
        prove_single_plants,
        prove_legal_plants,
        prove_unlisted_claim,
        prove_review_plants,
        prove_movement,
        prove_quiet_move,
        prove_tracked_plants,
        prove_inherited_record,
        prove_upstream_plants,
        prove_figure_pair,
        prove_citation_plant,
        prove_dense_plant,
        prove_duplicate_numbers,
        prove_immutability,
        prove_queue_age,
        prove_template_copy,
        prove_disposition,
        prove_anchors,
        prove_ignore_plant,
        prove_unrun_report,
        prove_empty_tree,
    )
    failures = sum(proof() for proof in proofs)
    for folder in built_folders:
        if not any(folder.iterdir()):
            folder.rmdir()
    print("every rule fires" if not failures else f"{failures} rule(s) do not work")
    return 1 if failures else 0


def main() -> int:
    """Audit the tree, or prove the audit."""
    if "--selftest" in sys.argv:
        return selftest()
    problems, advice = run(ROOT)
    unrun = unrun_checks(ROOT)
    if unrun:
        print(f"{len(unrun)} check(s) did not run on this tree, each named with what it needs:")
        for item in unrun:
            print(f"  {item}")
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
