"""Audit the tree against its own documentation and layout conventions.

A living document rots when a sentence that was true at writing stops being true after
reality moves through a path that never touches the file. The mechanical kinds of rot are
checked here, along with the shapes the rulebook fixes: budgets, the index contract over the
whole docs zone, names, the STATE schema, the version floor claims, the Python layout
conventions, the room every directory and root file has in the map or the baseline, the
coverage of the import graph the Dependency Rule contract runs over, the immutability of
records, the title beside every citation of one, and the decidable half of the docstring
convention. Decision records are exempt from
the freshness rules because they describe the past, which does not rot; what is held about
them is that nobody rewrites the past.

Run with --selftest first on any change to this file, because a check that never fires and a
check that cannot fire look identical.
"""

import ast
import posixpath
import re
import shutil
import subprocess
import sys
import tomllib
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
# In-flight work that has not moved in this long is either finished or stalled, and Now is
# for neither; the shorter horizon is what makes the sweep mechanical where it can be.
NOW_HORIZON_DAYS = 30
# Now is for in-flight work only; past this many entries the section is accreting, not tracking.
NOW_CAP = 5
# Bounded documents fail past this; AGENTS.md, docs/ARCHITECTURE.md, README.md, and the rulebook
# are the documents that grow with the system instead, a manual, a map, and the law it is held to.
BUDGET_LINES = 150
FREE_GROWING = {"AGENTS.md", "docs/ARCHITECTURE.md", "README.md", "docs/CONVENTIONS.md"}

BACKTICK = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
RECORD_NAME = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
DATED_RECORD_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")
# The numbered record folders: decisions/, this project's own, and inherited/, the template's
# own carried whole in a project built from it, keeping the template's numbers so the two
# sequences never meet. A template has no inherited folder.
NUMBERED_RECORD_FOLDERS = ("decisions", "inherited")
# The upstream file a project built from the template carries: one Open section, entries dated by
# heading with a kind, a pin, and four labeled parts, expiring on the same horizon as STATE.
UPSTREAM_ENTRY = re.compile(r"^### (\d{4}-\d{2}-\d{2}) (.+)$", re.MULTILINE)
UPSTREAM_KIND = re.compile(r"^Kind: (improvement|defect)$", re.MULTILINE)
UPSTREAM_PIN = re.compile(r"^Pin: [0-9a-f]{7,40}$", re.MULTILINE)
UPSTREAM_PARTS = ("**What it is", "**How the work surfaced it", "**Records checked")
UPSTREAM_WHY = ("**Why it is believed better", "**What was worked around")
UPSTREAM_ALIGNED = re.compile(r"^Aligned to .+ at (`?[0-9a-f]{7,40}`?|the host's own commit)\.?$", re.MULTILINE)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
DOTTED_MODULE = re.compile(r"[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)+")
TREE_FILE = re.compile(r"[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)+")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".ruff_cache", ".venv", "dist", "build"}
# Only a claim with the trailing plus is a floor claim; a bare version mention could be
# talking about anything, and a check may never imply more than it decides.
FLOOR_CLAIM = re.compile(r"Python (\d+\.\d+)\+")
# A changed diff line, added or removed; the +++ and --- headers are excluded by the lookahead
# and skipped by name where the diff is read. A record's changed lines are judged in pairs: a
# Status line may move, and a link target may move to one that resolves, because a path points
# at the present while the record's words describe the past.
CHANGED_LINE = re.compile(r"^[-+](?![-+])")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")
NUMPY_SECTION = re.compile(
    r"^[ \t]*(Parameters|Returns|Raises|Attributes|Yields|Warns|Notes|Usage|Examples|See Also|References)[ \t]*\n[ \t]*-{3,}[ \t]*$",
    re.MULTILINE,
)
TRIO = ("Parameters", "Returns", "Raises")
# This sentence dates the immutability rule's arrival in the tree's own history, so it is what
# the check searches for, never the function's name, which a child's past may already carry.
# Changing what the check covers changes this sentence, and the anchor moves forward with it.
IMMUTABILITY_SCOPE = "records held immutable beyond their Status line and a link target repaired to resolve: every file below a subfolder of docs/"
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
# A tracked file carries at most this many em dashes, because the plague arrives as clusters and a
# cluster is countable; the count runs here rather than in the workflow alone, so a tree with no
# remote is held to it. A file holding a NUL byte is binary and is not read for it.
EM_DASH_BUDGET = 2
EM_DASH = "\u2014".encode()
# The vocabulary the prose law bans, advised and never gated, because an honest domain term
# reads the same as a tell; the workflow's list, moved here so a tree with no remote hears it.
VOCABULARY = re.compile(
    r"paradigm shift|game.changer|ever-evolving|cutting.edge|\bdelve|\btapestry\b|\bsupercharge|\btransformative\b"
    r"|\bmultifaceted\b|\bmeticulous\b|\bparamount\b|\bembark\b|it.s worth noting|at the end of the day"
    r"|in today.s world|let.s dive|going forward|a testament to|marks a pivotal|plays a vital role|experts agree"
    r"|studies show|widely regarded as",
    re.IGNORECASE,
)
# What the two advisories skip: the workflows, the rulebook that lists the tells, and this
# script, which carries the list; a record is skipped by its depth under docs/.
VOCABULARY_SKIP = (".github/", "docs/CONVENTIONS.md", "scripts/audit_docs.py")
CODESPELL_SKIP = ".git,node_modules,.hypothesis,__pycache__,dist,package-lock.json,*.svg,*.png,*.ico,*.woff,*.woff2,*.map,decisions,claims,reviews,inherited,mockServiceWorker.js"
CODESPELL_IGNORE = "accreting,afterall"
# A prose paragraph that names this many references or more is an enumeration wearing prose, a
# list or a table with its rows run together; measured over the family and over a project built
# from it, everything at this count was a schema stated as prose or a set of bindings, and
# everything argued sat well below it. Whether a given paragraph is one of those stays with
# review, so the count advises and never gates.
DENSE_PARAGRAPH = 8
REFERENCE = re.compile(r"`[^`\n]+`|\[[^\]]*\]\([^)\s]+\)")
NOT_PROSE = ("#", "- ", "* ", "|", ">")


def git(*args: str) -> str:
    """One git call against the repository this file lives in; empty when git says no."""
    # The arguments are this script's own constants and git is the tool the family runs on.
    done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)  # noqa: S603, S607
    return done.stdout if done.returncode == 0 else ""


def tracked_files() -> list[str]:
    """Every tracked path, posix and relative to the root, so untracked local clutter never fires a check."""
    return [p for p in git("ls-files", "-z").split("\0") if p]


def drawn_entries(text: str) -> set[str]:
    """Every name drawn in a document's tree diagrams, directories without their trailing slash."""
    names: set[str] = set()
    for fence in FENCE.finditer(text):
        block = fence.group(1)
        if "──" not in block:
            continue
        for raw in block.splitlines():
            entry = raw.split("#", 1)[0].strip(" │├└─\t").rstrip("/")
            if entry:
                names.add(entry)
    return names


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


def check_record_names(problems: list[str]) -> None:
    """Records written after the cap arrived keep their filenames within it; carried folders are exempt."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return
    arrival = first_commit(RECORD_NAME_SCOPE, "scripts/audit_docs.py")
    added = added_commits("docs")
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
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


def aligned_at_host() -> bool:
    """Whether the upstream file aligns this tree at the host's own commit, as an arrow carried inside its style's repository is."""
    upstream = ROOT / "docs/UPSTREAM.md"
    return upstream.exists() and HOST_OWN_COMMIT in upstream.read_text(encoding="utf-8")


def check_dispositions(problems: list[str]) -> None:
    """Every record the inherited folder gained after adoption is cited by a record of the project's own."""
    inherited = ROOT / "docs/inherited"
    if not inherited.is_dir() or aligned_at_host() or not git("ls-tree", "-r", "--name-only", "HEAD", "--", "docs/inherited").strip():
        return
    cited: set[str] = set()
    for record in (ROOT / "docs/decisions").glob("*.md"):
        cited.update(INHERITED_CITATION.findall(record.read_text(encoding="utf-8")))
    uncited = [p for p in sorted(inherited.glob("*.md")) if RECORD_NAME.match(p.name) and p.name[:4] not in cited]
    if not uncited:
        return
    arrival = first_commit(DISPOSITION_SCOPE, "scripts/audit_docs.py")
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


def check_template_copies(problems: list[str]) -> None:
    """No record of the project's own is an inherited record's body under another number."""
    inherited = ROOT / "docs/inherited"
    decisions = ROOT / "docs/decisions"
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


def check_em_dashes(problems: list[str]) -> None:
    """Every tracked text file stays within the em dash budget, counted here so a tree with no remote is held to it."""
    for rel in tracked_files():
        path = ROOT / rel
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        count = data.count(EM_DASH)
        if count > EM_DASH_BUDGET:
            problems.append(f"{rel} carries {count} em dashes; the budget is {EM_DASH_BUDGET} per file")


def check_record_links(problems: list[str]) -> None:
    """Every relative link in a record of the project's own resolves; the inherited folder is checked where it was written."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.count("/") < 2 or rel.startswith("docs/inherited/"):
            continue
        check_links(problems, rel, path, path.read_text(encoding="utf-8"))


def advise_vocabulary(advice: list[str]) -> None:
    """The prose law's banned vocabulary in living prose and code, advised because an honest term reads like a tell."""
    for rel in tracked_files():
        path = ROOT / rel
        if rel.startswith(VOCABULARY_SKIP) or (rel.startswith("docs/") and rel.count("/") >= 2) or not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        for number, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            hit = VOCABULARY.search(line)
            if hit:
                advice.append(f"{rel}:{number}: inflated vocabulary or weasel attribution, {hit.group(0)!r}; the verdict is review's")


def advise_spelling(advice: list[str]) -> None:
    """Misspellings in living prose and code, advised where codespell is installed and named as not run elsewhere.

    The pass spawns a process, so it runs once per audit command rather than with the checks the
    proofs repeat forty times, and its proof calls it directly.
    """
    tool = shutil.which("codespell")
    if tool is None:
        return
    # The tool is a development dependency of the seat and the arguments are this script's own constants.
    done = subprocess.run([tool, "--skip", CODESPELL_SKIP, "--ignore-words-list", CODESPELL_IGNORE, "."], cwd=ROOT, capture_output=True, text=True, check=False)  # noqa: S603
    advice.extend(f"{line.strip()}; correct it, or name a domain term in the ignore list" for line in done.stdout.splitlines() if line.strip())


def local_main() -> bool:
    """Whether the tree has a local branch named main, which the stale-branch check reads against."""
    return bool(git("rev-parse", "--verify", "--quiet", "refs/heads/main").strip())


def check_stale_branches(problems: list[str]) -> None:
    """No local branch beside main and the ones checked out is already merged into main, or a landed branch outlives its landing."""
    if not local_main():
        return
    for line in git("for-each-ref", "--format=%(refname:short)%09%(worktreepath)", "refs/heads/").splitlines():
        name, _, worktree = line.partition("\t")
        if not name or name == "main" or worktree:
            continue
        if git("rev-list", "--count", f"main..{name}").strip() == "0":
            problems.append(
                f"branch {name} is already merged into main and still exists;"
                " a landed branch is deleted in the push that moves main, and a local one goes with it"
            )


def declared_names() -> str:
    """The project file and every source file as one text, where a dotted name may be declared rather than claimed.

    Dotted names declared in pyproject.toml or in the code itself (entry-point groups,
    contract layers) are not module claims, and their own readers verify the real ones.
    """
    pyproject = ROOT / "pyproject.toml"
    declared = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
    for source in ROOT.rglob("*.py"):
        if not any(part in SKIP_DIRS for part in source.parts):
            declared += source.read_text(encoding="utf-8", errors="ignore")
    return declared


def missing_module(token: str) -> bool:
    """Whether a dotted name under one of the Python roots names no module or package on disk."""
    for root in python_roots():
        if token.split(".")[0] != root.name:
            continue
        module_path = root.parent.joinpath(*token.split("."))
        if not (module_path.is_dir() or module_path.with_suffix(".py").exists()):
            return True
    return False


def check_budget(problems: list[str], rel: str, text: str) -> None:
    """A bounded document stays within the line budget; the free-growing ones are not measured."""
    if rel in FREE_GROWING:
        return
    lines = text.count("\n") + 1
    if lines > BUDGET_LINES:
        problems.append(f"{rel}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")


def check_backticked_claims(problems: list[str], rel: str, text: str, declared: str) -> None:
    """Every backticked path exists and every backticked module under a root is on disk."""
    for match in BACKTICK.finditer(text):
        token = match.group(1).strip()
        if looks_like_path(token) and not (ROOT / token.lstrip("./").rstrip("/")).exists():
            line = text.count("\n", 0, match.start()) + 1
            problems.append(f"{rel}:{line}: names `{token}`, which does not exist")
        elif DOTTED_MODULE.fullmatch(token) and token not in declared and missing_module(token):
            line = text.count("\n", 0, match.start()) + 1
            problems.append(f"{rel}:{line}: names the module `{token}`, which does not exist")


def check_tree_diagrams(problems: list[str], rel: str, text: str, basenames: set[str]) -> None:
    """Every file a tree diagram draws exists somewhere in the repository."""
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


def check_links(problems: list[str], rel: str, doc: Path, text: str) -> None:
    """Every relative link in the prose resolves.

    Links inside inline code spans are schema examples, not claims; the spans are blanked
    with same-length padding so reported line numbers stay true.
    """
    prose = BACKTICK.sub(lambda m: " " * len(m.group(0)), text)
    for match in LINK.finditer(prose):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        resolved = (doc.parent / target.split("#", 1)[0]).resolve()
        if not resolved.exists():
            line = prose.count("\n", 0, match.start()) + 1
            problems.append(f"{rel}:{line}: links to {target}, which does not resolve")


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


def advise_forms(advice: list[str]) -> None:
    """The form advisory over every living document, the spine and the flat documents under docs/."""
    docs = ROOT / "docs"
    rels = list(LIVING) + [f"docs/{f.name}" for f in sorted(docs.glob("*.md")) if docs.is_dir() and f"docs/{f.name}" not in LIVING]
    for rel in rels:
        path = ROOT / rel
        if path.exists():
            advise_dense_paragraphs(advice, rel, path.read_text(encoding="utf-8"))


def record_title(record: Path) -> str | None:
    """The title a record's heading states, after its number, or None where the heading is not in the form."""
    first = record.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    if not first.startswith("# ") or ". " not in first:
        return None
    return first.split(". ", 1)[1].strip()


def check_record_citations(problems: list[str], rel: str, doc: Path, text: str) -> None:
    """Every link to a record carries the record's title in the same paragraph, so the sentence stands without the click."""
    for paragraph in re.split(r"\n\s*\n", text):
        for match in LINK.finditer(paragraph):
            target = match.group(1).split("#", 1)[0]
            record = doc.parent / target
            if not RECORD_LINK.search(target) or not record.exists():
                continue
            title = record_title(record)
            if title is None or title in paragraph:
                continue
            line = text.count("\n", 0, text.find(match.group(0))) + 1
            problems.append(f"{rel}:{line}: cites {record.name[:4]} without its title; a citation carries the number and the title, {title}")


def standing_days(raw: str, binding: str, today: date) -> int:
    """How long a queued entry has stood unchanged, counted from the binding commit or the entry's own, whichever is later."""
    born = first_commit(STATE_TEXT.sub("", raw).strip(), "STATE.md")
    start = None if born is None else commit_date(binding if is_before(born, binding) else born)
    return (today - start).days if start is not None else 0


def check_state_entries(problems: list[str], text: str, today: date) -> None:
    """Every dated entry is within its section's horizon, and no queued entry has stood for two of them."""
    section = ""
    binding = first_commit(STATE_AGE_SCOPE, "scripts/audit_docs.py")
    for line_no, raw in enumerate(text.split("\n"), 1):
        if raw.startswith("## "):
            section = raw[3:].strip()
            continue
        stamp = STATE_DATE.search(raw)
        if not stamp:
            continue
        horizon = NOW_HORIZON_DAYS if section == "Now" else HORIZON_DAYS
        age = (today - datetime.strptime(stamp.group(1), "%Y-%m-%d").date()).days
        if age > horizon:
            problems.append(
                f"STATE.md:{line_no}: entry last verified {stamp.group(1)}, {age} days ago against the "
                f"{horizon}-day horizon of {section}; re-verify it against reality, then re-date or remove it"
            )
        if section == "Now" or binding is None:
            continue
        standing = standing_days(raw, binding, today)
        if standing > HORIZON_DAYS * 2:
            problems.append(
                f"STATE.md:{line_no}: entry has stood unchanged in {section} for {standing} days, two horizons; "
                "promote it to Now, write it as a decision record, or drop it"
            )


def check_state(problems: list[str], today: date) -> None:
    """The STATE schema: four sections, dated entries within their horizons, and a capped Now."""
    state = ROOT / "STATE.md"
    if not state.exists():
        return
    text = state.read_text(encoding="utf-8")
    sections = re.findall(r"^## (.+)$", text, re.MULTILINE)
    if sections != ["Now", "Next", "Deferred", "Blocked"]:
        problems.append(f"STATE.md: sections are {sections}, not the four the schema fixes")
    check_state_entries(problems, text, today)
    now_section = re.search(r"^## Now\n(.*?)(?=^## )", text, re.MULTILINE | re.DOTALL)
    if now_section:
        entries = len(re.findall(r"^- ", now_section.group(1), re.MULTILINE))
        if entries > NOW_CAP:
            problems.append(
                f"STATE.md: Now holds {entries} entries against the cap of {NOW_CAP}; "
                f"sweep finished work into git's memory"
            )


def check_documents(problems: list[str]) -> None:
    """Paths, links, budgets, and the STATE horizon across the living documents."""
    today = date.today()
    basenames = repo_basenames()
    declared = declared_names()
    for rel in LIVING:
        doc = ROOT / rel
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        check_budget(problems, rel, text)
        check_backticked_claims(problems, rel, text, declared)
        check_tree_diagrams(problems, rel, text, basenames)
        check_links(problems, rel, doc, text)
        check_record_citations(problems, rel, doc, text)
    check_state(problems, today)


def check_top_level_docs(problems: list[str], docs: Path, agents: str) -> None:
    """Every flat document under docs/ is registered, UPPERCASE, and within budget where it is bounded."""
    for f in sorted(docs.glob("*.md")):
        if f.name not in agents:
            problems.append(f"docs/{f.name}: not registered in the AGENTS.md index")
        if not f.stem.replace("-", "").isupper():
            problems.append(f"docs/{f.name}: organic documents are UPPERCASE markdown")
        if f.name not in ("ARCHITECTURE.md", "CONVENTIONS.md", "BASELINE.md", "UPSTREAM.md"):
            lines = f.read_text(encoding="utf-8").count("\n") + 1
            if lines > BUDGET_LINES:
                problems.append(f"docs/{f.name}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")
        if f"docs/{f.name}" not in LIVING:
            check_record_citations(problems, f"docs/{f.name}", f, f.read_text(encoding="utf-8"))


def check_record_numbers(problems: list[str], docs: Path) -> None:
    """Records in each numbered folder carry the record name and no two share a number.

    Numbers are unique within a folder and never compared across the two, which is the
    point of the split; a duplicate in the inherited folder means the copy is no longer
    the template's folder.
    """
    for folder_name in NUMBERED_RECORD_FOLDERS:
        records = docs / folder_name
        if not records.is_dir():
            continue
        advice = (
            "renumber the newer record" if folder_name == "decisions"
            else "recopy the folder whole from the template"
        )
        numbers: dict[str, str] = {}
        for f in sorted(records.glob("*.md")):
            if not RECORD_NAME.match(f.name):
                problems.append(f"docs/{folder_name}/{f.name}: records are named NNNN-short-kebab-title.md")
                continue
            num = f.name[:4]
            if num in numbers:
                problems.append(
                    f"docs/{folder_name}/: {numbers[num]} and {f.name} share the number {num}; {advice}"
                )
            numbers[num] = f.name


def check_below_top_level(problems: list[str], agents: str) -> None:
    """Below the top level, docs/ holds registered record folders of dated records and nothing else.

    The numbered folders and dated folders such as briefings or progress reports are each
    registered by their own row. A living document belongs at the top as a flat UPPERCASE
    file, where the naming and budget rules can see it, so anything else below a subfolder fails.
    """
    for path in tracked_files():
        if not path.startswith("docs/") or path.startswith("docs/decisions/"):
            continue
        if path.count("/") == 1:
            if not path.endswith(".md"):
                problems.append(f"{path}: docs/ holds markdown documents only; assets live where the baseline sends them")
            continue
        folder = "/".join(path.split("/")[:2])
        if f"({folder}/)" not in agents:
            problems.append(f"{path}: {folder}/ has no row in the AGENTS.md index; a subfolder of docs/ is a registered record folder or it does not exist")
        if folder != "docs/inherited" and not DATED_RECORD_NAME.match(path.rsplit("/", 1)[-1]):
            problems.append(
                f"{path}: a file below a docs/ subfolder is a dated record named YYYY-MM-DD-short-kebab-title.md; "
                f"a living document is a flat UPPERCASE file at the top of docs/"
            )


def check_docs_zone(problems: list[str]) -> None:
    """The index contract, budgets, and naming for everything under docs/."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
    check_top_level_docs(problems, docs, agents)
    check_record_numbers(problems, docs)
    check_below_top_level(problems, agents)


def check_upstream(problems: list[str]) -> None:
    """The upstream file's schema and horizon, where a project carries one."""
    path = ROOT / "docs/UPSTREAM.md"
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
    today = date.today()
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
    problems.extend(f"{label}: part {part}** missing" for part in UPSTREAM_PARTS if part not in chunk)
    if not any(why in chunk for why in UPSTREAM_WHY):
        problems.append(f"{label}: neither Why it is believed better nor What was worked around")
    age = (today - datetime.strptime(entry.group(1), "%Y-%m-%d").date()).days
    if age > HORIZON_DAYS:
        problems.append(
            f"{label}: past the {HORIZON_DAYS}-day horizon; re-verify against the template and re-date,"
            " or make it the project's own decision and delete it"
        )


def check_rooms(problems: list[str]) -> None:
    """Every tracked directory near the root, and every root file, has a room in the map or the baseline.

    The tree is read one level deep at the root and one level below each Python root, which is
    the depth the form draws; deeper structure is the code's own and the layout check holds it.
    A directory is housed when its name is drawn in the map's tree, or the baseline names it.
    """
    arch = ROOT / "docs/ARCHITECTURE.md"
    if not arch.exists():
        return
    named = drawn_entries(arch.read_text(encoding="utf-8"))
    baseline = ROOT / "docs/BASELINE.md"
    if baseline.exists():
        for match in BACKTICK.finditer(baseline.read_text(encoding="utf-8")):
            token = match.group(1).removeprefix("./")
            named.update(seg for seg in token.split("/") if seg)
    roots = {r.relative_to(ROOT).as_posix() for r in python_roots()}
    directories: set[str] = set()
    files: set[str] = set()
    for path in tracked_files():
        parts = path.split("/")
        if len(parts) == 1:
            files.add(parts[0])
            continue
        directories.add(parts[0])
        for depth in (1, 2):
            if "/".join(parts[:depth]) in roots and len(parts) > depth + 1:
                directories.add("/".join(parts[: depth + 1]))
    problems.extend(
        f"{directory}/: exists in the tree but has no room in docs/ARCHITECTURE.md or the baseline; draw it or fold it"
        for directory in sorted(directories)
        if directory.split("/")[-1] not in named
    )
    problems.extend(
        f"{name}: sits at the root but neither the map nor the baseline names it; give it a room or remove it"
        for name in sorted(files - {"AGENTS.md", "README.md", "STATE.md", "LICENSE"})
        if name not in named
    )


WORKING_TREE_DIRS = (".worktrees/", ".claude/worktrees/")


def check_ignored_working_trees(problems: list[str]) -> None:
    """The ignore file names every directory a second working tree may occupy."""
    ignore = ROOT / ".gitignore"
    lines = [line.strip() for line in ignore.read_text(encoding="utf-8").splitlines()] if ignore.exists() else []
    missing = [directory for directory in WORKING_TREE_DIRS if directory not in lines]
    if missing:
        problems.append(
            ".gitignore: a second working tree's directory is ignored before it is created;"
            f" the Working trees section names {' and '.join(WORKING_TREE_DIRS)}, missing {', '.join(missing)}"
        )


def check_import_graph(problems: list[str]) -> None:
    """The import graph the Dependency Rule contract runs over covers every module on disk.

    A contract reporting KEPT over a partial graph implies more than it decided, so the
    modules grimp sees under the contract's roots are held to the modules on disk.
    """
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return
    roots = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("tool", {}).get("importlinter", {}).get("root_packages", [])
    if not roots:
        return
    seen = graph_modules(problems, roots)
    if seen is None:
        return
    on_disk = modules_on_disk(problems, roots)
    unseen = sorted(on_disk - seen)
    if unseen:
        problems.append(
            f"the import graph covers {len(on_disk) - len(unseen)} of {len(on_disk)} modules under the contract roots, "
            f"so the Dependency Rule contract decides less than it reports; unseen: {', '.join(unseen[:5])}"
        )


def graph_modules(problems: list[str], roots: list[str]) -> set[str] | None:
    """The modules the import graph sees under the roots, or None with the reason it could not be built."""
    try:
        import grimp
    except ImportError:
        problems.append("the import graph library is not installed, so the contract's coverage cannot be verified; install the dev group")
        return None
    for base in (ROOT / "src", ROOT):
        if base.is_dir() and str(base) not in sys.path:
            sys.path.insert(0, str(base))
    try:
        graph = grimp.build_graph(*roots, include_external_packages=False)
    except Exception as error:  # noqa: BLE001  # whatever stops the graph stops the contract too, and is reported as such
        problems.append(f"the import graph could not be built ({error}); install the project before auditing")
        return None
    return set(graph.modules)


def modules_on_disk(problems: list[str], roots: list[str]) -> set[str]:
    """Every module under the contract roots as it sits on disk, dotted the way the graph names it."""
    on_disk: set[str] = set()
    for root in roots:
        home = next((b for b in (ROOT / "src", ROOT) if b.joinpath(*root.split(".")).is_dir()), None)
        if home is None:
            problems.append(f"{root}: named as an import-linter root, yet no directory matches it")
            continue
        for module in home.joinpath(*root.split(".")).rglob("*.py"):
            if "__pycache__" in module.parts:
                continue
            parts = list(module.relative_to(home).with_suffix("").parts)
            on_disk.add(".".join(parts[:-1] if parts[-1] == "__init__" else parts))
    return on_disk


def check_record_immutability(problems: list[str]) -> None:
    """A record changes only on its Status line or at a link target that resolves, in the working tree and in every commit since this scope arrived.

    The rule binds from the commit that brought its current scope sentence into the tree, found
    in git's own history, so an adopting project is held from its adoption forward, never
    re-litigates a past it did not write under the rule, and is never caught by a widened scope
    reaching behind its own arrival. A shallow clone cannot show that history, so it fails rather
    than quietly checking less.
    """
    if not (ROOT / "docs").is_dir():
        return
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        problems.append("the clone is shallow, so record history cannot be checked; fetch the full history")
        return
    for where, diff in record_diffs():
        flag_illegal_edits(problems, where, diff)


def record_diffs() -> list[tuple[str, str]]:
    """The diff of docs/ in the working tree and in every commit since the immutability scope arrived.

    Every subfolder of docs/ is a record folder, so the diff is read over docs/ and only
    files below a subfolder count; the flat living documents at the top change freely.
    """
    arrivals = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_docs.py").split()
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


def record_of(header: str) -> str:
    """The record a diff header names, or nothing when the file is a flat living document at the top of docs/."""
    path = header[6:]
    below = path.split("docs/", 1)[1] if "docs/" in path else ""
    return path if "/" in below else ""


def record_hunks(diff: str) -> list[tuple[str, list[str], list[str]]]:
    """Every hunk that changes a record, as the record's path with its removed and its added lines."""
    hunks: list[tuple[str, list[str], list[str]]] = []
    current = ""
    hunk: tuple[str, list[str], list[str]] | None = None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = record_of(line)
        if line.startswith(("+++ b/", "@@")):
            hunk = (current, [], []) if current else None
            if hunk is not None:
                hunks.append(hunk)
            continue
        if hunk is not None and CHANGED_LINE.match(line):
            (hunk[1] if line[0] == "-" else hunk[2]).append(line[1:])
    return [h for h in hunks if h[1] or h[2]]


def target_resolves(where: str, record: str, target: str) -> bool:
    """Whether a link target written in the record resolves, in the working tree or in the commit named by where."""
    path = posixpath.normpath(posixpath.join(posixpath.dirname(record), target.split("#", 1)[0]))
    if where == "the working tree":
        return (Path(git("rev-parse", "--show-toplevel").strip()) / path).exists()
    return bool(git("ls-tree", "--full-tree", where, "--", path).strip())


def legal_pair(where: str, record: str, old: str, new: str) -> bool:
    """A changed line is legal when only its Status moved, or only its link targets moved and each new target resolves."""
    if old.startswith("Status: ") and new.startswith("Status: "):
        return True
    if LINK_TARGET.sub("]()", old) != LINK_TARGET.sub("]()", new):
        return False
    return all(target_resolves(where, record, target) for target in LINK_TARGET.findall(new))


def flag_illegal_edits(problems: list[str], where: str, diff: str) -> None:
    """Every record the diff changes beyond its Status line or a link target that resolves, reported once each."""
    flagged: set[str] = set()
    for record, minus, plus in record_hunks(diff):
        legal = len(minus) == len(plus) and all(legal_pair(where, record, old, new) for old, new in zip(minus, plus, strict=True))
        if not legal and record not in flagged:
            flagged.add(record)
            problems.append(
                f"{record}: edited beyond its Status line in {where}; a record is immutable, so supersede it instead,"
                " or repair a link target to one that resolves"
            )


def section_entries(body: str) -> list[str]:
    """The names a NumPy section lists, read from the lines at its own indent; None. lists nothing."""
    lines = [line for line in body.split("\n") if line.strip()]
    if not lines:
        return []
    base = min(len(line) - len(line.lstrip()) for line in lines)
    names: list[str] = []
    for line in lines:
        if len(line) - len(line.lstrip()) != base:
            continue
        head = line.strip().split(" :", 1)[0].split(":", 1)[0].strip()
        if head and head != "None.":
            names.append(head.lstrip("*"))
    return names


def check_rhythm(problems: list[str], rel: str, lines: list[str], node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, doc: str) -> None:
    """The house docstring rhythm, held byte by byte where a rule can see it.

    The exemplars open with a blank line after the header, a lone triple quote, and a blank
    line; they close with a blank line, a lone triple quote, and a blank line before the body;
    every section header stands after two blank lines; and every parameter entry is typed as
    name : type. Each of those is a shape, so each is decided here rather than reviewed.
    """
    opening = node.body[0]
    start, end = opening.lineno, opening.end_lineno or opening.lineno
    where = f"{rel}:{start}: {node.name}"
    if lines[start - 1].strip() != '"""' or lines[end - 1].strip() != '"""':
        problems.append(f"{where}'s docstring opens and closes with a triple quote alone on its line")
        return
    if start < 2 or lines[start - 2].strip():
        problems.append(f"{where}'s docstring follows a blank line after the header")
    if lines[start].strip():
        problems.append(f"{where}'s docstring opens with a blank line after the triple quote")
    if lines[end - 2].strip():
        problems.append(f"{where}'s docstring closes with a blank line before the triple quote")
    if len(node.body) > 1 and end < len(lines) and lines[end].strip():
        problems.append(f"{where}'s docstring is followed by a blank line before the body")
    body = doc.split("\n")
    for i, raw in enumerate(body):
        if NUMPY_SECTION.match(raw + "\n" + (body[i + 1] if i + 1 < len(body) else "")) and (i < 2 or body[i - 1].strip() or body[i - 2].strip()):
            problems.append(f"{where}'s {raw.strip()} section stands after two blank lines")


def check_docstrings(problems: list[str]) -> None:
    """The decidable half of the docstring convention: rhythm, the trio together, and names that match the code.

    Whether a docstring says something true, and which classes warrant a Usage block, stay
    with review; what is held here is the house rhythm of blank lines and lone triple quotes,
    that a function documenting any of Parameters, Returns, or Raises documents all three,
    that Parameters names exactly the signature with every entry typed, and that an
    Attributes section names only attributes the class declares.
    """
    for root in python_roots():
        for source in sorted(root.rglob("*.py")):
            if "__pycache__" in source.parts:
                continue
            check_source_docstrings(problems, source.relative_to(ROOT).as_posix(), source.read_text(encoding="utf-8"))


def check_source_docstrings(problems: list[str], rel: str, text: str) -> None:
    """The docstring convention over one source file: no module docstring, and every documented node in shape."""
    lines = text.split("\n")
    tree = ast.parse(text)
    # A module carries no docstring in this dialect; its name and its room in the map say
    # what it is, and only a script run as a command, which lives outside these roots,
    # opens with one.
    if ast.get_docstring(tree) is not None:
        problems.append(f"{rel}:1: a module carries no docstring; its name and its room in the map say what it is, and only a script opens with one")
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        doc = ast.get_docstring(node, clean=False)
        if not doc:
            continue
        check_rhythm(problems, rel, lines, node, doc)
        sections = docstring_sections(doc)
        if isinstance(node, ast.ClassDef):
            check_attributes(problems, rel, node, sections)
            continue
        check_trio(problems, rel, node, sections)
        if "Parameters" in sections:
            check_parameters(problems, rel, node, sections["Parameters"])


def docstring_sections(doc: str) -> dict[str, str]:
    """Each NumPy section of a docstring by name, with the text that runs to the next header."""
    marks = list(NUMPY_SECTION.finditer(doc))
    return {
        m.group(1): doc[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(doc)]
        for i, m in enumerate(marks)
    }


def check_attributes(problems: list[str], rel: str, node: ast.ClassDef, sections: dict[str, str]) -> None:
    """A class's Attributes section names only attributes the class declares."""
    if "Attributes" not in sections:
        return
    declared = {t.target.id for t in node.body if isinstance(t, ast.AnnAssign) and isinstance(t.target, ast.Name)}
    stray = [n for n in section_entries(sections["Attributes"]) if n not in declared]
    if stray:
        problems.append(f"{rel}:{node.lineno}: {node.name} documents attributes {stray} that the class does not declare")


def check_trio(problems: list[str], rel: str, node: ast.FunctionDef | ast.AsyncFunctionDef, sections: dict[str, str]) -> None:
    """A function documenting any of Parameters, Returns, or Raises documents all three."""
    present = [s for s in TRIO if s in sections]
    if present and len(present) != len(TRIO):
        problems.append(
            f"{rel}:{node.lineno}: {node.name} documents {present} alone; a full docstring carries "
            f"Parameters, Returns, and Raises together, None. where a section is empty"
        )


def check_parameters(problems: list[str], rel: str, node: ast.FunctionDef | ast.AsyncFunctionDef, section: str) -> None:
    """The Parameters section names exactly the signature, in order, with every entry typed."""
    arguments = node.args
    ordered = [*arguments.posonlyargs, *arguments.args, arguments.vararg, *arguments.kwonlyargs, arguments.kwarg]
    signature = [a.arg for a in ordered if a is not None and a.arg not in ("self", "cls")]
    documented = section_entries(section)
    if documented != signature:
        problems.append(f"{rel}:{node.lineno}: {node.name} documents parameters {documented} but its signature has {signature}")
    entries = [line for line in section.split("\n") if line.strip()]
    base = min((len(line) - len(line.lstrip()) for line in entries), default=0)
    untyped = [
        line.strip() for line in entries
        if len(line) - len(line.lstrip()) == base and line.strip() != "None." and " : " not in line
    ]
    if untyped:
        problems.append(f"{rel}:{node.lineno}: {node.name} lists parameters without a type ({', '.join(untyped)}); an entry reads name : type")


def check_layout(problems: list[str]) -> list[Path]:
    """Folder purity and door-only __init__ files, the Python layout conventions, over a tree that exists.

    The audit says which roots it held, and fails when the tree's shape leaves it nothing to
    hold, because a run that examined nothing must not look like one that found nothing.
    """
    roots = python_roots()
    src = ROOT / "src"
    if src.is_dir():
        loose = sorted(p.name for p in src.iterdir() if p.suffix == ".py")
        if loose:
            problems.append(f"src/: holds loose modules ({', '.join(loose)}); the form is one package directory under src/")
        if len(roots) != 1:
            problems.append(f"src/: holds {len(roots)} package directories; the form is exactly one, so the layout has one tree to hold")
    elif not roots:
        problems.append("no app/ or src/ package tree exists for the layout conventions to hold, so this audit decides nothing about layout")
    for root in roots:
        for directory in [root, *[p for p in root.rglob("*") if p.is_dir()]]:
            if directory.name == "__pycache__" or directory == root:
                continue
            check_purity(problems, directory)
            check_door(problems, directory / "__init__.py")
    return roots


def check_purity(problems: list[str], directory: Path) -> None:
    """A directory below a root holds subpackages or modules, never both."""
    subpackages = [
        p for p in directory.iterdir()
        if p.is_dir() and p.name != "__pycache__" and any(p.rglob("*.py"))
    ]
    modules = [p for p in directory.iterdir() if p.suffix == ".py" and p.name != "__init__.py"]
    if subpackages and modules:
        rel = directory.relative_to(ROOT)
        problems.append(f"{rel}: holds both subpackages and modules; a directory holds one or the other")


def check_door(problems: list[str], init: Path) -> None:
    """An __init__.py below a root is a door: imports and a docstring, nothing else."""
    if not init.exists():
        return
    tree = ast.parse(init.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue
        rel = init.relative_to(ROOT)
        problems.append(f"{rel}: an __init__.py is a door and only re-exports")
        break


def declared_python() -> str | None:
    """The version ruff's target-version pins, which is the tree's one number."""
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return None
    match = re.search(r'target-version = "py(\d)(\d+)"', pyproject.read_text(encoding="utf-8"))
    return f"{match.group(1)}.{match.group(2)}" if match else None


def check_version_story(problems: list[str]) -> None:
    """Every floor claim in living prose names the version the tree declares."""
    declared = declared_python()
    if declared is None:
        return
    for rel in LIVING:
        path = ROOT / rel
        if not path.exists():
            continue
        problems.extend(
            f"{rel}: claims Python {claimed}+ while the tree declares {declared};"
            " the version story is one number"
            for claimed in FLOOR_CLAIM.findall(path.read_text(encoding="utf-8"))
            if claimed != declared
        )


# What a check needs before it can run. A check whose need is absent is reported as not run,
# with the need named, so a clean verdict never hides a check the tree gave nothing to check.
CHECK_NEEDS = (
    ("check_state", "STATE.md"),
    ("check_upstream", "docs/UPSTREAM.md"),
    ("check_dispositions", "docs/inherited"),
    ("check_template_copies", "docs/inherited"),
    ("check_rooms", "docs/ARCHITECTURE.md"),
    ("check_docs_zone", "docs"),
    ("check_record_links", "docs"),
)


def unrun_checks() -> list[str]:
    """Every check the tree gave nothing to run, each named with what it needs."""
    unrun = [f"{name} did not run: {need} is absent from this tree" for name, need in CHECK_NEEDS if not (ROOT / need).exists()]
    if (ROOT / "docs/inherited").exists() and aligned_at_host():
        unrun.append(
            "check_dispositions did not run: docs/UPSTREAM.md aligns this arrow at the host's own commit,"
            " so the family audit holds its inherited folder and no re-alignment gains it a record"
        )
    if not python_roots():
        unrun.append("check_layout and check_docstrings did not run: no package root is on disk")
    pyproject = ROOT / "pyproject.toml"
    roots = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("tool", {}).get("importlinter", {}).get("root_packages", []) if pyproject.exists() else []
    if not roots:
        unrun.append("check_import_graph did not run: pyproject.toml names no importlinter root_packages")
    if shutil.which("codespell") is None:
        unrun.append("advise_spelling did not run: codespell is not on PATH; the development dependencies carry it, or pipx install codespell")
    if not local_main():
        unrun.append("check_stale_branches did not run: no local branch named main")
    if not git("remote").strip():
        unrun.append(
            "the workflow did not run: this repository names no remote, so its landed-branches step,"
            " the one check beyond the gate's commands it carries, ran nowhere"
        )
    if declared_python() is None:
        unrun.append("check_version_story did not run: pyproject.toml pins no ruff target-version")
    return unrun


def run() -> tuple[list[str], list[str], list[Path]]:
    """Every disagreement between the tree and its conventions, every piece of advice, and the package roots the layout was held over."""
    problems: list[str] = []
    advice: list[str] = []
    advise_forms(advice)
    advise_vocabulary(advice)
    check_documents(problems)
    check_record_links(problems)
    check_docs_zone(problems)
    check_record_names(problems)
    check_upstream(problems)
    check_dispositions(problems)
    check_template_copies(problems)
    check_em_dashes(problems)
    check_rooms(problems)
    check_ignored_working_trees(problems)
    check_stale_branches(problems)
    held = check_layout(problems)
    check_import_graph(problems)
    check_record_immutability(problems)
    check_docstrings(problems)
    check_version_story(problems)
    return problems, advice, held


# Plants, each an untracked file the glob-reading checks see, and the finding it must raise.
FILE_PLANTS = [
    ("docs/lowercase-planted.md", "# Planted\n", "organic documents are UPPERCASE markdown"),
    ("docs/PLANTED.md", "# Planted\n", "docs/PLANTED.md: not registered in the AGENTS.md index"),
    ("docs/PLANTED.md", "# Planted\n" + "line\n" * 150, f"docs/PLANTED.md: 152 lines against the {BUDGET_LINES}-line budget"),
    ("docs/decisions/bad-name-planted.md", "# Bad\n", "records are named NNNN-short-kebab-title.md"),
    (
        "docs/decisions/0093-planted-with-a-title-so-long-that-it-runs-past-the-seventy-two-character-cap.md",
        "# 0093. Planted\n\nStatus: Accepted\nDate: 2026-01-01\n",
        f"the cap is {NAME_CAP}",
    ),
]

# Plants appended to a living document, whose bytes are restored afterwards.
APPEND_PLANTS = [
    ("AGENTS.md", "\nNames `docs/GHOST-PLANTED.md` in passing.\n", "names `docs/GHOST-PLANTED.md`, which does not exist"),
    ("AGENTS.md", "\nLinks [nowhere](docs/NOWHERE-PLANTED.md) in passing.\n", "links to docs/NOWHERE-PLANTED.md, which does not resolve"),
    (
        "docs/ARCHITECTURE.md",
        "\n```text\nplanted/\n└── ghost_planted_file.py\n```\n",
        "the tree names ghost_planted_file.py, which exists nowhere in this repository",
    ),
    ("docs/BASELINE.md", "line\n" * 160, f"lines against the {BUDGET_LINES}-line budget; split by fission"),
]

# Plants the tracked-tree checks can see; each is intent-to-added for one run.
TRACKED_PLANTS = [
    ("stray-planted/note.txt", "nobody gave this a room\n", "stray-planted/: exists in the tree but has no room"),
    ("ROGUE-PLANTED.txt", "nobody named this\n", "ROGUE-PLANTED.txt: sits at the root but neither the map nor the baseline names it"),
    ("docs/planted.png", "not a document\n", "docs/planted.png: docs/ holds markdown documents only"),
    ("docs/planted-folder/GUIDE.md", "# Guide\n", "docs/planted-folder/ has no row in the AGENTS.md index"),
    ("docs/planted-folder/GUIDE.md", "# Guide\n", "a file below a docs/ subfolder is a dated record named YYYY-MM-DD-short-kebab-title.md"),
    ("docs/PLANTED-DASHES.md", "\u2014 \u2014 \u2014\n", "docs/PLANTED-DASHES.md carries 3 em dashes; the budget is 2 per file"),
]

# A source file carrying one defect per docstring rule, planted under the first package root.
DOCSTRING_PLANT = (
    '"""A module docstring where none belongs."""\n\n\n'
    "def only_parameters(a: int, b: int) -> int:\n\n"
    '    """\n\n    Adds.\n\n\n    Parameters\n    ----------\n    a : int\n        One.\n\n    b\n        Two.\n\n    c : int\n        Three.\n\n    """\n\n'
    "    return a + b\n\n\n"
    "def bad_rhythm(a: int) -> int:\n"
    '    """Adds one.\n\n    Returns\n    -------\n    int\n    """\n'
    "    return a + 1\n\n\n"
    "class Holder:\n\n"
    '    """\n\n    Holds.\n\n    Attributes\n    ----------\n    seen : int\n        Declared.\n\n    ghost : int\n        Not declared.\n\n    """\n\n'
    "    seen: int = 0\n"
)
DOCSTRING_EXPECTS = (
    "a module carries no docstring",
    "only_parameters documents ['Parameters'] alone",
    "only_parameters documents parameters ['a', 'b', 'c'] but its signature has ['a', 'b']",
    "only_parameters lists parameters without a type (b)",
    "bad_rhythm's docstring opens and closes with a triple quote alone on its line",
    "Holder's Attributes section stands after two blank lines",
    "Holder documents attributes ['ghost'] that the class does not declare",
)

UPSTREAM_HEAD = "# Upstream\n\nAligned to Planted at 0123456789ab.\n\nEvery entry is a lead, not a verdict.\n\n## Open\n\n"
UPSTREAM_PARTS_TEXT = (
    "**What it is.** x.\n\n**How the work surfaced it.** x.\n\n"
    "**Why it is believed better.** x.\n\n**Records checked.** None.\n"
)


def wrong(message: str) -> int:
    """Report one broken rule and count it."""
    print(f"WRONG: {message}")
    return 1


def expect(problems: list[str], needle: str, label: str) -> int:
    """Zero when a finding carries the needle, else one reported failure."""
    if any(needle in p for p in problems):
        return 0
    return wrong(f"{label} did not raise {needle!r}")


def restore(path: Path, original: bytes | None) -> None:
    """Put a borrowed file back as it was, or remove it when it did not exist."""
    if original is None:
        path.unlink(missing_ok=True)
    else:
        path.write_bytes(original)


def remove_planted(path: Path, stop: Path) -> None:
    """Remove a planted file and every directory it emptied below the stop directory."""
    path.unlink(missing_ok=True)
    parent = path.parent
    while parent != stop and parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
        parent = parent.parent


def prove_file_plants() -> int:
    """Each untracked plant raises its finding and leaves no trace."""
    failures = 0
    for rel, content, needle in FILE_PLANTS:
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        try:
            failures += expect(run()[0], needle, f"plant {rel}")
        finally:
            remove_planted(target, ROOT)
    return failures


def prove_append_plants() -> int:
    """Each plant appended to a living document raises its finding, and the document's bytes come back."""
    failures = 0
    for rel, appended, needle in APPEND_PLANTS:
        target = ROOT / rel
        if not target.exists():
            print(f"append plant skipped: {rel} is not in this tree")
            continue
        original = target.read_bytes()
        target.write_bytes(original + appended.encode())
        try:
            failures += expect(run()[0], needle, f"plant on {rel}")
        finally:
            target.write_bytes(original)
    return failures


def prove_tracked_plants() -> int:
    """Each plant the tracked-tree checks read raises its finding; nothing reaches a commit."""
    failures = 0
    for rel, content, needle in TRACKED_PLANTS:
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        git("add", "-N", "--", rel)
        try:
            failures += expect(run()[0], needle, f"tracked plant {rel}")
        finally:
            git("rm", "--cached", "-q", "--", rel)
            remove_planted(target, ROOT)
    return failures


def prove_twin_numbers() -> int:
    """Two records sharing one number are reported, naming both."""
    taken = {p.name[:4] for p in (ROOT / "docs/decisions").glob("*.md")}
    free = next(f"{n:04d}" for n in range(900, 10000) if f"{n:04d}" not in taken)
    twins = [ROOT / f"docs/decisions/{free}-planted-twin-{side}.md" for side in ("a", "b")]
    try:
        for twin in twins:
            twin.write_text(f"# {free}. Planted twin\n\nStatus: Accepted\nDate: 2026-01-01\n", encoding="utf-8")
        return expect(run()[0], f"share the number {free}", "the twin records")
    finally:
        for twin in twins:
            twin.unlink(missing_ok=True)


def state_variants() -> list[tuple[str, str, str]]:
    """Each STATE.md plant as a replacement pair and the finding it raises."""
    six = "".join(f"- Planted in-flight work {n} ({date.today().isoformat()})\n" for n in range(6))
    return [
        ("## Next", "## Queue", "not the four the schema fixes"),
        ("## Blocked\n", "## Blocked\n\n- Planted stale blocked work (2025-01-01)\n", f"against the {HORIZON_DAYS}-day horizon of Blocked"),
        ("## Now\n", "## Now\n\n" + six, f"entries against the cap of {NOW_CAP}"),
    ]


def prove_state_plants() -> int:
    """The STATE schema's decidable rules fire: the four sections, the horizon, and the cap on Now."""
    state = ROOT / "STATE.md"
    if not state.exists():
        print("STATE plants skipped: no STATE.md in this tree")
        return 0
    failures = 0
    original = state.read_bytes()
    text = original.decode("utf-8").replace("\r\n", "\n")
    for old, new, needle in state_variants():
        if old not in text:
            failures += wrong(f"STATE.md lacks {old!r}, so its plant cannot be placed")
            continue
        state.write_bytes(text.replace(old, new, 1).encode())
        try:
            failures += expect(run()[0], needle, f"STATE plant {needle!r}")
        finally:
            state.write_bytes(original)
    print("queue age firing case skipped: no queued entry in this tree has two horizons of history")
    return failures


def upstream_variants() -> list[tuple[str, str | None]]:
    """Each UPSTREAM.md plant and the finding it raises, None for one that must pass."""
    today = date.today().isoformat()
    entry = f"### {today} Planted entry\n\nKind: defect\nPin: 0123456789ab\n\n"
    return [
        (UPSTREAM_HEAD + "Nothing open.\n", None),
        (UPSTREAM_HEAD + entry + UPSTREAM_PARTS_TEXT, None),
        ("# Upstream\n\nEvery entry is a lead, not a verdict.\n\n## Open\n\nNothing open.\n", "no Aligned line"),
        ("# Upstream\n\nAligned to Planted at 0123456789ab.\n\nNo section.\n", "no ## Open section"),
        (UPSTREAM_HEAD + "Nothing here.\n", "Open holds entries or the words Nothing open."),
        (UPSTREAM_HEAD + "Nothing open.\n\n" + entry + UPSTREAM_PARTS_TEXT, "beside open entries"),
        (UPSTREAM_HEAD + f"### {today} Planted entry\n\nPin: 0123456789ab\n\n" + UPSTREAM_PARTS_TEXT, "no Kind line"),
        (UPSTREAM_HEAD + f"### {today} Planted entry\n\nKind: defect\n\n" + UPSTREAM_PARTS_TEXT, "no Pin line"),
        (UPSTREAM_HEAD + entry + "**What it is.** x.\n\n**Why it is believed better.** x.\n", "part **How the work surfaced it** missing"),
        (UPSTREAM_HEAD + entry + "**What it is.** x.\n\n**How the work surfaced it.** x.\n\n**Records checked.** None.\n", "neither Why it is believed better"),
        (UPSTREAM_HEAD + "### 2026-01-01 Planted entry\n\nKind: defect\nPin: 0123456789ab\n\n" + UPSTREAM_PARTS_TEXT, f"past the {HORIZON_DAYS}-day horizon"),
    ]


def prove_upstream_plants() -> int:
    """A legal UPSTREAM.md passes and each rule of its schema fires; the path is borrowed and given back."""
    failures = 0
    upstream = ROOT / "docs/UPSTREAM.md"
    original = upstream.read_bytes() if upstream.exists() else None
    try:
        for text, needle in upstream_variants():
            upstream.write_text(text, encoding="utf-8")
            hits = [p for p in run()[0] if "UPSTREAM" in p]
            if needle is None and hits:
                failures += wrong(f"a legal UPSTREAM.md raised {hits[:2]}")
            elif needle is not None:
                failures += expect(hits, needle, "an UPSTREAM.md plant")
    finally:
        restore(upstream, original)
    return failures


def prove_docstring_plants() -> int:
    """Each decidable docstring rule fires against one planted source file."""
    roots = python_roots()
    if not roots:
        print("docstring plants skipped: no package root in this tree")
        return 0
    target = roots[0] / "planted_selftest.py"
    target.write_text(DOCSTRING_PLANT, encoding="utf-8")
    try:
        problems = run()[0]
        return sum(expect(problems, needle, "the docstring plant") for needle in DOCSTRING_EXPECTS)
    finally:
        target.unlink()


def prove_layout_plants() -> int:
    """A directory holding both subpackages and modules, and an __init__.py that is not a door, are reported."""
    roots = python_roots()
    if not roots:
        print("layout plants skipped: no package root in this tree")
        return 0
    failures = 0
    mixed = roots[0] / "planted_mixed"
    # The mixed directory carries doors so the import graph sees it and reports nothing extra.
    planted = {
        roots[0] / "planted_door" / "__init__.py": "planted = 1\n",
        mixed / "__init__.py": "",
        mixed / "inner" / "__init__.py": "",
        mixed / "inner" / "leaf.py": "leaf = 1\n",
        mixed / "loose.py": "loose = 1\n",
    }
    try:
        for path, content in planted.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        problems = run()[0]
        failures += expect(problems, "an __init__.py is a door and only re-exports", "the door plant")
        failures += expect(problems, "holds both subpackages and modules", "the mixed-directory plant")
    finally:
        for path in planted:
            remove_planted(path, roots[0])
    return failures


def prove_src_shape() -> int:
    """A loose module under src/ is reported, where the tree has a src/ layout."""
    src = ROOT / "src"
    if not src.is_dir():
        print("src plant skipped: this tree has no src/ layout")
        return 0
    loose = src / "loose_planted.py"
    loose.write_text("loose = 1\n", encoding="utf-8")
    try:
        return expect(run()[0], "src/: holds loose modules (loose_planted.py)", "the loose module plant")
    finally:
        loose.unlink()


def prove_version_plant() -> int:
    """A floor claim that disagrees with the declared version is reported."""
    declared = declared_python()
    readme = ROOT / "README.md"
    if declared is None or not readme.exists():
        print("version plant skipped: no declared version or no README.md in this tree")
        return 0
    claimed = "3.11" if declared != "3.11" else "3.12"
    original = readme.read_bytes()
    readme.write_bytes(original + f"\nRequires Python {claimed}+ here.\n".encode())
    try:
        return expect(run()[0], f"claims Python {claimed}+ while the tree declares {declared}", "the version plant")
    finally:
        readme.write_bytes(original)


def prove_module_plant() -> int:
    """A backticked module under a package root that is not on disk is reported."""
    roots = python_roots()
    agents = ROOT / "AGENTS.md"
    if not roots or not agents.exists():
        print("module plant skipped: no package root or no AGENTS.md in this tree")
        return 0
    token = f"{roots[0].name}.ghost_planted_module"
    original = agents.read_bytes()
    agents.write_bytes(original + f"\nNames the module `{token}` in passing.\n".encode())
    try:
        return expect(run()[0], f"names the module `{token}`, which does not exist", "the module plant")
    finally:
        agents.write_bytes(original)


def prove_citation_plant() -> int:
    """A record cited without its title is reported, and the same citation with the title passes."""
    record = next(iter(sorted((ROOT / "docs/decisions").glob("*.md"))), None)
    agents = ROOT / "AGENTS.md"
    title = record_title(record) if record is not None else None
    if record is None or title is None or not agents.exists():
        print("citation plants skipped: no titled record or no AGENTS.md in this tree")
        return 0
    failures = 0
    original = agents.read_bytes()
    number = record.name[:4]
    try:
        agents.write_bytes(original + f"\nSee [decision {number}](docs/decisions/{record.name}) in passing.\n".encode())
        failures += expect(run()[0], f"cites {number} without its title", "the bare citation plant")
        agents.write_bytes(original + f"\nSee [decision {number}, {title}](docs/decisions/{record.name}) in passing.\n".encode())
        if any("without its title" in p for p in run()[0]):
            failures += wrong("a citation carrying the record's title was reported as bare")
    finally:
        agents.write_bytes(original)
    return failures


def prove_dense_plant() -> int:
    """A prose paragraph naming eight references is advised, and the same eight names as a list are not."""
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        print("form plants skipped: no AGENTS.md in this tree")
        return 0
    names = [f"`planted_{n}`" for n in range(DENSE_PARAGRAPH)]
    failures = 0
    original = agents.read_bytes()
    # The tree may carry dense paragraphs of its own, so the plant is judged by what it adds.
    before = len(run()[1])
    try:
        agents.write_bytes(original + f"\nThe planted paragraph names {', '.join(names)} in one breath.\n".encode())
        added = [a for a in run()[1] if f"names {DENSE_PARAGRAPH} references" in a and "AGENTS.md" in a]
        if len(run()[1]) != before + 1 or not added:
            failures += wrong("a prose paragraph naming eight references raised no advice of its own")
        agents.write_bytes(original + ("\n" + "".join(f"- {name}\n" for name in names)).encode())
        if len(run()[1]) != before:
            failures += wrong("a list of eight names was advised as a dense paragraph")
    finally:
        agents.write_bytes(original)
    return failures


def prove_immutability() -> int:
    """A body edit to an accepted record fails and a Status flip alone passes.

    Immutability is a fact about a record's history, so this is the one plant that cannot
    build its subject; it selects the lowest-numbered accepted record of the project's own by
    that property, never by a number written here.
    """
    record = next(
        (p for p in sorted((ROOT / "docs/decisions").glob("*.md")) if "\nStatus: Accepted\n" in p.read_text(encoding="utf-8")),
        None,
    )
    if record is None:
        print("immutability plants skipped: no accepted record of this project's own to plant on")
        return 0
    failures = 0
    original = record.read_bytes()
    try:
        record.write_bytes(original + b"\nplanted body edit\n")
        failures += expect(run()[0], "edited beyond its Status line", f"a body edit to {record.name}")
        record.write_bytes(original.replace(b"Status: Accepted", b"Status: Superseded by 0999", 1))
        if any("edited beyond its Status line" in p for p in run()[0]):
            failures += wrong(f"a Status flip on {record.name} was reported as an illegal edit")
    finally:
        record.write_bytes(original)
    return failures


def free_number(folder: Path, start: int) -> str:
    """The lowest record number from the start that no record in the folder uses, for a plant that must not collide."""
    taken = {p.name[:4] for p in folder.glob("*.md")}
    return next(f"{n:04d}" for n in range(start, 10000) if f"{n:04d}" not in taken)


def prove_template_copy() -> int:
    """A record of the project's own whose body is an inherited record's is reported, whatever its number and status."""
    decisions = ROOT / "docs/decisions"
    if not decisions.is_dir():
        print("template copy plant skipped: no docs/decisions in this tree")
        return 0
    inherited_dir = ROOT / "docs/inherited"
    inherited_dir.mkdir(exist_ok=True)
    free = free_number(inherited_dir, 1)
    own = free_number(decisions, 900)
    body = "\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\nPlanted twice.\n"
    template = inherited_dir / f"{free}-planted-template.md"
    copy = decisions / f"{own}-planted-template.md"
    try:
        template.write_text(f"# {free}. Planted template" + body, encoding="utf-8")
        copy.write_text(f"# {own}. Planted template" + body.replace("Status: Accepted", "Status: Superseded by 0999"), encoding="utf-8")
        return expect(run()[0], f"is the template's record docs/inherited/{template.name}", "the template copy plant")
    finally:
        copy.unlink(missing_ok=True)
        remove_planted(template, ROOT / "docs")


def prove_disposition() -> int:
    """A record the inherited folder gains with no citing record fails, and the same record cited passes.

    The firing case needs a folder that already stood in history, so it runs where the tree carries
    one, the rehearsal's child among them, and is named as skipped in the template, whose folder the
    plant builds, and in an arrow aligned at the host's own commit, which gains nothing by re-alignment.
    """
    decisions = ROOT / "docs/decisions"
    if not decisions.is_dir():
        print("disposition plants skipped: no docs/decisions in this tree")
        return 0
    failures = 0
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
        elif aligned_at_host():
            print("disposition firing case skipped: this arrow is aligned at the host's own commit and gains nothing by re-alignment")
        else:
            failures += expect(run()[0], "cited by no record of this project's own", "the gained record plant")
        citing.write_text(
            f"# {own}. Planted disposition\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\n"
            f"[Inherited {free}, Planted gained](../inherited/{gained.name}) bound nothing here.\n",
            encoding="utf-8",
        )
        if any("cited by no record" in p for p in run()[0]):
            failures += wrong("a gained record cited by a record of this project's own was reported as uncited")
    finally:
        citing.unlink(missing_ok=True)
        remove_planted(gained, ROOT / "docs")
    return failures


def record_with_link(folders: tuple[str, ...]) -> tuple[Path, str] | None:
    """The first record of the project's own in the folders that carries a relative link, with that link's target."""
    for folder in folders:
        for record in sorted((ROOT / folder).glob("*.md")):
            for target in LINK_TARGET.findall(record.read_text(encoding="utf-8")):
                if not target.startswith(("http://", "https://", "#", "mailto:")):
                    return record, target
    return None


def prove_link_repair() -> int:
    """A link target repaired to one that resolves passes; a changed link text or a target that does not resolve fails."""
    found = record_with_link(("docs/decisions",))
    if found is None:
        print("link repair plants skipped: no record of this project's own carries a relative link")
        return 0
    record, target = found
    failures = 0
    original = record.read_bytes()
    text = original.decode("utf-8")
    other = "../CONVENTIONS.md" if target.split("#", 1)[0] != "../CONVENTIONS.md" else "../ARCHITECTURE.md"
    try:
        record.write_bytes(text.replace(f"]({target})", f"]({other})", 1).encode("utf-8"))
        if any("edited beyond its Status line" in p for p in run()[0]):
            failures += wrong(f"repairing a link target in {record.name} to one that resolves was reported as an illegal edit")
        record.write_bytes(text.replace(f"]({target})", "](../GHOST-PLANTED.md)", 1).encode("utf-8"))
        failures += expect(run()[0], "edited beyond its Status line", f"a link target in {record.name} pointed at a ghost")
        record.write_bytes(text.replace(f"]({target})", f" planted]({target})", 1).encode("utf-8"))
        failures += expect(run()[0], "edited beyond its Status line", f"a link's text in {record.name} changed")
    finally:
        record.write_bytes(original)
    return failures


def prove_record_link_plant() -> int:
    """A dead link in a record of the project's own is reported, and the same link in an inherited record is not."""
    decisions = ROOT / "docs/decisions"
    if not decisions.is_dir():
        print("record link plants skipped: no docs/decisions in this tree")
        return 0
    inherited_dir = ROOT / "docs/inherited"
    inherited_dir.mkdir(exist_ok=True)
    own = decisions / f"{free_number(decisions, 900)}-planted-dead-link.md"
    carried = inherited_dir / f"{free_number(inherited_dir, 1)}-planted-dead-link.md"
    body = "\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Decision\n\nSee [gone](../GONE-PLANTED.md)"
    failures = 0
    try:
        own.write_text(f"# {own.name[:4]}. Planted dead link" + body + " here.\n", encoding="utf-8")
        carried.write_text(f"# {carried.name[:4]}. Planted dead link" + body + " there.\n", encoding="utf-8")
        problems = run()[0]
        failures += expect(problems, f"docs/decisions/{own.name}:8: links to ../GONE-PLANTED.md, which does not resolve", "the dead link plant")
        if any("docs/inherited/" in p and "does not resolve" in p for p in problems):
            failures += wrong("a dead link in an inherited record was reported; inherited records are checked where they were written")
    finally:
        own.unlink(missing_ok=True)
        remove_planted(carried, ROOT / "docs")
    return failures


def prove_vocabulary_plant() -> int:
    """A banned word appended to the guide is advised, and the bytes come back."""
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        print("vocabulary plant skipped: no AGENTS.md in this tree")
        return 0
    original = agents.read_bytes()
    agents.write_bytes(original + b"\nWe delve into it here.\n")
    try:
        if any("inflated vocabulary" in a and "'delve'" in a and "AGENTS.md" in a for a in run()[1]):
            return 0
        return wrong("a banned word appended to AGENTS.md raised no vocabulary advice")
    finally:
        agents.write_bytes(original)


def prove_spelling_plant() -> int:
    """A misspelling appended to the README is advised where codespell is installed, and the bytes come back."""
    readme = ROOT / "README.md"
    if shutil.which("codespell") is None or not readme.exists():
        print("spelling plant skipped: codespell is not on PATH or no README.md in this tree")
        return 0
    original = readme.read_bytes()
    readme.write_bytes(original + b"\nThe reciever waits here.\n")  # codespell:ignore reciever
    try:
        advice: list[str] = []
        advise_spelling(advice)
        if any("reciever ==> receiver" in a for a in advice):  # codespell:ignore reciever
            return 0
        return wrong("a misspelling appended to README.md raised no spelling advice")
    finally:
        readme.write_bytes(original)


def prove_stale_branch() -> int:
    """A local branch already merged into main is reported, and the branch is removed again."""
    if not local_main():
        print("stale branch plant skipped: no local branch named main")
        return 0
    name = "planted-stale-branch"
    git("branch", name, "main")
    try:
        return expect(run()[0], f"branch {name} is already merged into main", "the stale branch plant")
    finally:
        git("branch", "-D", name)


def prove_no_remote_report() -> int:
    """A repository naming no remote reports the workflow as not run; the rehearsal's child is where this fires."""
    if git("remote").strip():
        print("no-remote report skipped: this repository names a remote, so the rehearsal's child proves it")
        return 0
    if any("names no remote" in line for line in unrun_checks()):
        return 0
    return wrong("a repository with no remote did not report the workflow as not run")


def prove_anchors() -> int:
    """Each history-reading rule's scope sentence is dated by the commit that introduced it."""
    failures = 0
    for name, scope in (("immutability", IMMUTABILITY_SCOPE), ("queue age", STATE_AGE_SCOPE), ("filename cap", RECORD_NAME_SCOPE), ("disposition", DISPOSITION_SCOPE)):
        arrival = git("log", "--reverse", "--format=%H", "-S", scope, "--", "scripts/audit_docs.py").split()
        if not arrival:
            print(f"anchor plant skipped: the {name} scope sentence has not reached history yet")
        elif scope in git("show", f"{arrival[0]}^:scripts/audit_docs.py"):
            failures += wrong(f"the {name} anchor is older than the commit that introduced the current scope")
    print("import graph plants skipped: the graph library sees every module on disk, and a root it cannot import stops the build first")
    return failures


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
        return expect(run()[0], "Working trees section", "ignore plant")
    finally:
        ignore.write_bytes(original)


def prove_unrun_report() -> int:
    """Hiding a check's need names the check as not run, and the file comes back."""
    state = ROOT / "STATE.md"
    if not state.exists():
        print("unrun plant skipped: no STATE.md in this tree")
        return 0
    if any("check_state did not run" in line for line in unrun_checks()):
        return wrong("check_state was reported as not run while STATE.md is present")
    original = state.read_bytes()
    state.unlink()
    try:
        if any("check_state did not run" in line for line in unrun_checks()):
            return 0
        return wrong("hiding STATE.md did not report check_state as not run")
    finally:
        state.write_bytes(original)


def selftest() -> int:
    """Prove each rule fires against a planted defect, then leave no trace.

    A plant builds what it needs and removes what it built, so the proof holds in a project
    built from this template as well as in the template; a rule that can only be planted with
    history, or that the tooling cannot be made to miss, is named as skipped rather than
    counted as proven.
    """
    baseline, _, _ = run()
    if baseline:
        print("the unplanted tree is not clean, so nothing can be proven until the audit passes:")
        for p in baseline[:5]:
            print(f"  {p}")
        return 1
    proofs = (
        prove_file_plants,
        prove_append_plants,
        prove_tracked_plants,
        prove_twin_numbers,
        prove_state_plants,
        prove_upstream_plants,
        prove_docstring_plants,
        prove_layout_plants,
        prove_src_shape,
        prove_version_plant,
        prove_module_plant,
        prove_citation_plant,
        prove_dense_plant,
        prove_vocabulary_plant,
        prove_spelling_plant,
        prove_immutability,
        prove_link_repair,
        prove_record_link_plant,
        prove_template_copy,
        prove_disposition,
        prove_anchors,
        prove_ignore_plant,
        prove_stale_branch,
        prove_no_remote_report,
        prove_unrun_report,
    )
    failures = sum(proof() for proof in proofs)
    print("every rule fires" if not failures else f"{failures} rule(s) do not work")
    return 1 if failures else 0


def main() -> int:
    """Run every check and report each disagreement between the tree and its conventions, or prove the checks."""
    if "--selftest" in sys.argv:
        return selftest()
    problems, advice, held = run()
    advise_spelling(advice)
    unrun = unrun_checks()
    if unrun:
        print(f"{len(unrun)} check(s) did not run on this tree, each named with what it needs:")
        for item in unrun:
            print(f"  {item}")
    if advice:
        print(f"advisory, {len(advice)} item(s), decides nothing and gates nothing:")
        for item in advice:
            print(f"  {item}")
    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The tree disagrees with its own conventions.")
        return 1
    over = ", ".join(r.relative_to(ROOT).as_posix() for r in held) or "no package tree"
    print(f"The tree agrees with its own conventions (layout held over {over}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
