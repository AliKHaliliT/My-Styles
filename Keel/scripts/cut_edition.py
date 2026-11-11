"""Cut an edition of this project, the tree a public repository receives.

The editions document, docs/EDITIONS.md, is the law this script carries out. A tier says how much of the project
leaves the workshop, and below the snapshot a version says whether what leaves names the style it was built under.

    python scripts/cut_edition.py snapshot DESTINATION
    python scripts/cut_edition.py hand-made DESTINATION [--silent]
    python scripts/cut_edition.py bare DESTINATION [--silent]
    python scripts/cut_edition.py --selftest

A cut is taken from the last commit and assembled whole before a byte is written, so a refusal leaves the
destination as it was. Nothing here commits, pushes or deletes, because publishing the destination is the owner's.
"""

import ast
import configparser
import io
import posixpath
import re
import subprocess
import sys
import tempfile
import tokenize
import tomllib
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

USAGE = """usage: python scripts/cut_edition.py TIER DESTINATION [--silent]
  TIER is snapshot, hand-made or bare; the whole tier is the repository itself and needs no cut
  --silent cuts the version that names nothing of the style, for the hand-made and the bare tier
  DESTINATION is a folder outside the repository that holds nothing yet"""
TIERS = ("snapshot", "hand-made", "bare")

# What the style has a project keep, withheld from every tier below the snapshot: the guide and the state, the
# documents and the records, the audits and this tool, the word list the spelling advisory reads, and the workflow
# that runs the style's gate. A project names its own withholdings in the list below, one path to a line.
STYLE_FILES = ("AGENTS.md", "STATE.md", ".codespellignore", ".github/workflows/ci.yml")
STYLE_FOLDERS = ("docs/", "edition/")
STYLE_TOOLS = (
    "scripts/audit_docs.py",
    "scripts/audit_inquiry.py",
    "scripts/cut_edition.py",
    "scripts/audit-docs.mjs",
    "scripts/audit-docs-selftest.mjs",
    "scripts/cut-edition.mjs",
)
WITHHELD_LIST = "edition/withheld.txt"
# Files the public receives in another form than the workshop keeps, laid over the hand-made tier at the same path.
OVERLAY = "edition/overlay/"

# The words that name the style where nothing else does, advised in a silent edition and never deciding, since
# each of them is also a word a product may use of itself.
VOCABULARY = re.compile(r"\b(?:rulebook|prose law|docs audit|invariants ledger|upstream entry|re-alignment|decision record)\b", re.IGNORECASE)
FAMILY = re.compile(r"My-Styles")

NOTICES = {
    "hand-made": "This repository is the project's hand-made edition, its code as written, published without the records, the rules and the gates it was built under.",
    "bare": "This repository is the project's bare edition, its code with comments and docstrings stripped, published without the records, the rules and the gates it was built under.",
}
# What a bare README keeps beside its opening: how to run the thing, and under what terms.
BARE_SECTIONS = ("Getting Started", "License")
FENCE = re.compile(r"^\s*(?:```|~~~)")
RULE = re.compile(r"\n---\s*$")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[`*])")
LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")
ENTRY = re.compile(r"^((?:[│ ] {3})*)(├──|└──) (\S+)(.*)$")
SPACER = re.compile(r"^[│ ]*│[│ ]*$")
# A comment a tool reads is an instruction and stays; only a reason written after it is a remark.
DIRECTIVE = re.compile(r"#\s*(?:!|type:|noqa\b|pragma:|pylint:|mypy:|ruff:|fmt:|isort:|nosec\b|-\*-|vim:)")
# The longest path this system is sure to write. Past it a write can fail halfway, so a cut that would reach it is
# refused before a byte is written.
PATH_LIMIT = 248 if sys.platform == "win32" else 4000
# Kinds that hold no comment by their nature, left out of the list of what a bare cut carried as written.
PLAIN = (".md", ".json", ".typed", ".lock")
TERMS = ("LICENSE", "COPYING", "NOTICE", "README")

type Comment = tuple[int, int, str]
type Span = tuple[int, int, int, str, bool]
type Wanted = Callable[[str], bool] | None


@dataclass
class Cut:
    """One cut in progress: what was asked, what it holds so far, and what it has to say."""

    tier: str
    silent: bool
    nested: bool
    edition: dict[str, bytes] = field(default_factory=dict)
    withheld: list[str] = field(default_factory=list)
    foreign: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)
    advice: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


@dataclass
class Drawn:
    """One line of a drawn tree: an entry at its depth, a spacer between entries, or a line the tree does not own."""

    kind: str
    depth: int = 0
    name: str = ""
    tail: str = ""
    raw: str = ""


def git(*args: str, data: bytes | None = None) -> bytes:
    """One git call in this project's tree, answered in bytes; empty when git says no."""
    # The arguments are this script's own constants and git is the tool the family runs on.
    done = subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True, check=False)  # noqa: S603, S607
    return done.stdout if done.returncode == 0 else b""


def tracked() -> list[str]:
    """Every tracked path of this project, posix and relative to its root."""
    return [path for path in git("ls-files", "-z").decode("utf-8").split("\0") if path]


def blobs(paths: list[str]) -> dict[str, bytes]:
    """The committed bytes of each path, read from the last commit in one call, so a cut never depends on how a checkout ends its lines."""
    asked = "".join(f"HEAD:./{path}\n" for path in paths).encode("utf-8")
    stream = io.BytesIO(git("cat-file", "--batch", data=asked))
    found: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            continue
        found[path] = stream.read(int(header[2]))
        stream.read(1)
    return found


def project_list(paths: list[str]) -> list[str]:
    """The paths this project withholds beyond the style's own, one to a line in its list, a folder by its trailing slash."""
    if WITHHELD_LIST not in paths:
        return []
    text = blobs([WITHHELD_LIST]).get(WITHHELD_LIST, b"").decode("utf-8")
    return [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def is_withheld(path: str, own: list[str]) -> bool:
    """Whether a path belongs to the workshop: the style's files, folders and tools, or a path the project's list names."""
    if path in STYLE_FILES or path in STYLE_TOOLS or path.startswith(STYLE_FOLDERS):
        return True
    return any(path == entry.rstrip("/") or path.startswith(entry.rstrip("/") + "/") for entry in own)


def nested_roots(paths: list[str]) -> list[str]:
    """The projects kept inside this one, each a folder below the root that carries a guide of its own."""
    roots = sorted(path[: -len("/AGENTS.md")] for path in paths if path.endswith("/AGENTS.md"))
    return [root for root in roots if not any(root.startswith(f"{other}/") for other in roots)]


def as_text(data: bytes) -> str | None:
    """Bytes as text where they are text, None for a binary file, which a cut copies and never reads."""
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def fenced(text: str) -> list[tuple[bool, str]]:
    """A document as runs of prose and fenced blocks in order, each fenced run with its fence lines."""
    runs: list[tuple[bool, str]] = []
    inside = False
    current: list[str] = []
    for line in text.splitlines(keepends=True):
        if not FENCE.match(line):
            current.append(line)
        elif inside:
            runs.append((True, "".join([*current, line])))
            current, inside = [], False
        else:
            runs.append((False, "".join(current)))
            current, inside = [line], True
    runs.append((inside, "".join(current)))
    return [(kind, run) for kind, run in runs if run]


def split_sections(text: str) -> list[tuple[str, str]]:
    """A document as its opening and its second-level sections, each a title with its body; a heading inside a fence is never one."""
    parts: list[tuple[str, list[str]]] = [("", [])]
    for is_fence, run in fenced(text):
        for line in run.splitlines(keepends=True):
            if not is_fence and line.startswith("## "):
                parts.append((line[3:].strip(), []))
            parts[-1][1].append(line)
    return [(title, "".join(lines)) for title, lines in parts]


def with_notice(opening: str, notice: str) -> str:
    """The opening with the edition's notice as its last paragraph, above the rule that closes it where it has one."""
    body = opening.rstrip()
    closing = ""
    if RULE.search(body):
        body = RULE.sub("", body).rstrip()
        closing = "---\n\n"
    return f"{body}\n\n{notice}\n\n{closing}"


def silent_opening(cut: Cut, opening: str) -> str:
    """The opening without the sentences that name the family, each one reported so the owner sees what left."""
    kept: list[str] = []
    for paragraph in opening.split("\n\n"):
        if not FAMILY.search(paragraph) or paragraph.lstrip().startswith(("#", "!", "<", "|", "-", "`")):
            kept.append(paragraph)
            continue
        sentences = SENTENCE_END.split(paragraph)
        cut.notes.extend(f"README.md: cut for naming the family: {s.strip()}" for s in sentences if FAMILY.search(s))
        staying = [sentence for sentence in sentences if not FAMILY.search(sentence)]
        if staying:
            kept.append(" ".join(staying))
    return "\n\n".join(kept)


def rewrite_readme(cut: Cut, text: str) -> str:
    """The project's README as the tier publishes it: the section that points at the rulebook cut, the bare tier down to its opening and how to run it, and the opening carrying the notice or losing what names the family."""
    parts = split_sections(text)
    kept = [(title, body) for title, body in parts if not title.startswith("Conventions")]
    if len(kept) != len(parts):
        cut.notes.append("README.md: the Conventions section was cut, since it points at documents the edition withholds")
    if cut.tier == "bare":
        kept = [(title, body) for title, body in kept if not title or title.startswith(BARE_SECTIONS)]
    opening = silent_opening(cut, kept[0][1]) if cut.silent else with_notice(kept[0][1], NOTICES[cut.tier])
    whole = "".join([opening.rstrip("\n") + "\n\n", *(body for _, body in kept[1:])])
    return RULE.sub("", whole.rstrip()) + "\n"


def follows(items: list[Drawn], index: int, level: int) -> bool:
    """Whether an entry at this level is still to come before the tree climbs above it."""
    for item in items[index + 1 :]:
        if item.kind == "entry" and item.depth <= level:
            return item.depth == level
    return False


def bars(items: list[Drawn], index: int, depth: int) -> str:
    """The columns to the left of a line, a bar wherever a folder above it has more to show."""
    return "".join("│   " if follows(items, index, level) else "    " for level in range(depth))


def parse_tree(lines: list[str], gone: Callable[[str], bool]) -> tuple[list[Drawn], int]:
    """The lines of a drawn tree as items, an entry the edition withholds left out with everything drawn under it."""
    items: list[Drawn] = []
    stack: list[str] = []
    cut_depth: int | None = None
    dropped = 0
    for line in lines:
        match = ENTRY.match(line)
        if match is None:
            if cut_depth is None or not SPACER.match(line):
                items.append(Drawn("spacer" if SPACER.match(line) else "other", raw=line))
            continue
        depth = len(match.group(1)) // 4
        if cut_depth is not None and depth > cut_depth:
            dropped += 1
            continue
        cut_depth = None
        del stack[depth:]
        stack.append(match.group(3).rstrip("/"))
        if gone("/".join(stack)):
            cut_depth, dropped = depth, dropped + 1
            continue
        items.append(Drawn("entry", depth, match.group(3), match.group(4)))
    return items, dropped


def render_tree(items: list[Drawn]) -> list[str]:
    """The items of a tree drawn again, each entry closing its folder when nothing follows it there."""
    lines: list[str] = []
    for index, item in enumerate(items):
        if item.kind == "other":
            lines.append(item.raw)
        elif item.kind == "entry":
            glyph = "├──" if follows(items, index, item.depth) else "└──"
            lines.append(f"{bars(items, index, item.depth)}{glyph} {item.name}{item.tail}")
        elif index and items[index - 1].kind == "entry":
            ahead = next((later for later in items[index + 1 :] if later.kind == "entry"), None)
            if ahead is not None:
                lines.append(f"{bars(items, index, ahead.depth)}│")
    return lines


def redraw_trees(cut: Cut, path: str, text: str, present: set[str]) -> str:
    """A document whose drawn trees no longer show what the edition withholds, their branches redrawn around the gap."""

    def gone(entry: str) -> bool:
        here = entry in present or any(kept.startswith(f"{entry}/") for kept in present)
        return not here and (entry in cut.withheld or any(held.startswith(f"{entry}/") for held in cut.withheld))

    runs: list[str] = []
    total = 0
    for is_fence, run in fenced(text):
        items, dropped = parse_tree(run.splitlines(), gone) if is_fence and "──" in run else ([], 0)
        total += dropped
        runs.append("\n".join(render_tree(items)) + "\n" if dropped else run)
    if total:
        cut.notes.append(f"{path}: {total} line(s) of a drawn tree left out, the branches redrawn around them")
    return "".join(runs)


def unlink(cut: Cut, path: str, text: str, present: set[str]) -> str:
    """A document with every link into a path the edition does not hold turned back into its words; an image it cannot show is a problem, since nothing stands in for a picture."""
    here = posixpath.dirname(path)
    count = 0

    def held(target: str) -> bool:
        return target in present or target == "." or any(kept.startswith(f"{target}/") for kept in present)

    def swap(match: re.Match[str]) -> str:
        nonlocal count
        target = match.group(3).split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            return match.group(0)
        if held(posixpath.normpath(posixpath.join(here, target))):
            return match.group(0)
        if match.group(1):
            cut.problems.append(f"{path}: the image {match.group(3)} is not in the edition, and nothing stands in for a picture")
            return match.group(0)
        count += 1
        return match.group(2)

    rewritten = "".join(run if is_fence else LINK.sub(swap, run) for is_fence, run in fenced(text))
    if count:
        cut.notes.append(f"{path}: {count} link(s) into withheld paths turned back into their words")
    return rewritten


def rewrite_documents(cut: Cut, present: set[str]) -> None:
    """Every Markdown document the edition keeps, rewritten for what the edition holds: the README by its schema, drawn trees without withheld entries, and links into withheld paths turned back into words."""
    for path in sorted(cut.edition):
        text = as_text(cut.edition[path]) if path.endswith(".md") and path not in cut.foreign else None
        if text is None:
            continue
        if path == "README.md":
            text = rewrite_readme(cut, text)
        text = unlink(cut, path, redraw_trees(cut, path, text, present), present)
        cut.edition[path] = text.encode("utf-8")


def remove_spans(source: str, spans: list[Span]) -> str:
    """A text without the spans named: a line a span empties is dropped, a line a span shortens loses the space left at its end, and every other line stands as it was."""
    by_row: dict[int, list[Span]] = {}
    for span in spans:
        by_row.setdefault(span[0], []).append(span)
    kept: list[str] = []
    for row, line in enumerate(source.splitlines(keepends=True)):
        if row not in by_row:
            kept.append(line)
            continue
        body = line.rstrip("\r\n")
        ending = line[len(body) :]
        whole = False
        for _, start, end, replacement, covers in sorted(by_row[row], key=lambda span: -span[1]):
            body = body[:start] + replacement + body[end:]
            whole = whole or covers
        if not whole and body.strip():
            kept.append(body.rstrip() + ending)
    return "".join(kept)


def named_blocks(comments: list[Comment], lines: list[str], wanted: Callable[[str], bool]) -> list[Comment]:
    """The comments that go for naming what is wanted gone, each with the block it stands in: a run of comment lines is one remark, and a remark that names the style leaves whole."""

    def alone(comment: Comment) -> bool:
        return not lines[comment[0]][: comment[1]].strip()

    taken: list[Comment] = []
    block: list[Comment] = []
    for comment in [*comments, (-9, 0, "")]:
        joins = bool(block) and comment[0] == block[-1][0] + 1 and alone(block[-1]) and alone(comment)
        if block and not joins:
            taken.extend(block if any(wanted(text) for _, _, text in block) else [])
            block = []
        if comment[0] >= 0:
            block.append(comment)
    return taken


def python_comments(source: str) -> list[Comment]:
    """Every comment of a Python text a strip may take: a directive stays, and only a reason written after it is offered."""
    found: list[Comment] = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT:
            continue
        row, column = token.start[0] - 1, token.start[1]
        if not DIRECTIVE.match(token.string):
            found.append((row, column, token.string))
        elif (reason := token.string.find("#", 1)) > 0:
            found.append((row, column + reason, token.string[reason:]))
    return found


def characters(line: str, column: int) -> int:
    """A column the parser counted in bytes, as the same place counted in characters."""
    return len(line.encode("utf-8")[:column].decode("utf-8", "ignore"))


def is_docstring(node: ast.AST) -> bool:
    """Whether a statement is a bare string, which is a docstring where it opens a module, a class or a function."""
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def documented(tree: ast.AST) -> list[ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef]:
    """Every module, class and function of a tree that opens with a docstring."""
    owners = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    return [node for node in ast.walk(tree) if isinstance(node, owners) and node.body and is_docstring(node.body[0])]


def docstring_spans(source: str) -> list[Span]:
    """The docstring of every module, class and function as spans, three dots standing in where a docstring was a whole body."""
    lines = source.splitlines()
    spans: list[Span] = []
    for owner in documented(ast.parse(source)):
        node = owner.body[0]
        stand_in = "..." if len(owner.body) == 1 and not isinstance(owner, ast.Module) else ""
        first, last = node.lineno - 1, (node.end_lineno or node.lineno) - 1
        start, end = characters(lines[first], node.col_offset), characters(lines[last], node.end_col_offset or 0)
        spans.extend(blank_neighbours(lines, first, last))
        if first == last:
            spans.append((first, start, end, stand_in, False))
            continue
        spans.append((first, start, len(lines[first]), stand_in, False))
        spans.extend((row, 0, len(lines[row]), "", True) for row in range(first + 1, last))
        spans.append((last, 0, end, "", False))
    return spans


def blank_neighbours(lines: list[str], first: int, last: int) -> list[Span]:
    """The blank lines that stood around a docstring, which go with it so a body opens where its header ends."""
    rows: list[int] = []
    row = first - 1
    while row >= 0 and not lines[row].strip():
        rows.append(row)
        row -= 1
    row = last + 1
    while row < len(lines) and not lines[row].strip():
        rows.append(row)
        row += 1
    return [(row, 0, 0, "", True) for row in rows]


def strip_python(source: str, wanted: Wanted) -> str:
    """A Python text without its comments and docstrings, or without only the comments that name what is wanted gone."""
    lines = source.splitlines()
    comments = python_comments(source)
    chosen = comments if wanted is None else named_blocks(comments, lines, wanted)
    spans: list[Span] = [(row, column, len(lines[row]), "", False) for row, column, _ in chosen]
    return remove_spans(source, spans + (docstring_spans(source) if wanted is None else []))


def proven_python(before: str, after: str, wanted: Wanted) -> bool:
    """Whether a stripped Python text parses to the tree its source parses to, docstrings apart where the whole strip took them; comments are no part of a tree, so nothing else can have gone."""
    expected = ast.parse(before)
    if wanted is None:
        for owner in documented(expected):
            if len(owner.body) == 1 and not isinstance(owner, ast.Module):
                owner.body[0] = ast.Expr(ast.Constant(...))
            else:
                del owner.body[0]
    return ast.dump(expected) == ast.dump(ast.parse(after))


def toml_opens(line: str) -> int:
    """The column where a TOML line's comment opens, a hash inside a quoted string never being one; a string that runs across lines is beyond this reader, and the proof catches a cut made inside one."""
    quote = ""
    skip = False
    for column, char in enumerate(line):
        if skip:
            skip = False
        elif quote:
            skip = char == "\\" and quote == '"'
            quote = "" if char == quote else quote
        elif char in "\"'":
            quote = char
        elif char == "#":
            return column
    return -1


def edge_opens(line: str) -> int:
    """The column of a comment in a file that holds one only on a line a hash begins."""
    return 0 if line.startswith("#") else -1


def hash_opens(line: str) -> int:
    """The column of a comment in a file that holds one on a line whose first mark is a hash."""
    return len(line) - len(line.lstrip()) if line.lstrip().startswith("#") else -1


def mark_opens(line: str) -> int:
    """The column of a comment in a file that holds one on a line whose first mark is a hash or a semicolon."""
    return len(line) - len(line.lstrip()) if line.lstrip().startswith(("#", ";")) else -1


OPENS: dict[str, Callable[[str], int]] = {"toml": toml_opens, "ini": mark_opens, "marks": mark_opens, "edge": edge_opens, "hash": hash_opens}


def kind_of(path: str) -> str:
    """The kind of text a path holds, for the kinds a strip can prove itself on, or the empty string."""
    name = posixpath.basename(path)
    if name.endswith((".py", ".pyi")):
        return "python"
    if name.endswith((".toml", ".ini", ".cfg")):
        return "toml" if name.endswith(".toml") else "ini"
    if name in (".gitignore", ".dockerignore", ".gitattributes"):
        return "edge"
    if name == ".editorconfig":
        return "marks"
    if name.startswith(".env") or (name.startswith("requirements") and name.endswith(".txt")):
        return "hash"
    return ""


def parsed_ini(text: str) -> dict[str, dict[str, str]]:
    """An INI text as the sections and values a reader of it gets."""
    parser = configparser.RawConfigParser(strict=False)
    parser.read_string(text)
    return {section: dict(parser.items(section)) for section in parser.sections()} | {"": dict(parser.defaults())}


def proven_lines(kind: str, before: str, after: str) -> bool:
    """Whether a text stripped a line at a time still says what its source says: the same values where a parser can read both, the same lines beside the comments where the format has no more to it."""
    if kind == "toml":
        return tomllib.loads(before) == tomllib.loads(after)
    if kind == "ini":
        return parsed_ini(before) == parsed_ini(after)
    opens = OPENS[kind]
    return [line for line in before.splitlines() if opens(line) < 0] == [line for line in after.splitlines() if opens(line) < 0]


def stripped(kind: str, source: str, wanted: Wanted) -> str | None:
    """A text of a known kind after its strip, or None where the strip could not prove it took comments and docstrings alone."""
    try:
        if kind == "python":
            after = strip_python(source, wanted)
            return after if proven_python(source, after, wanted) else None
        lines = source.splitlines()
        comments = [(row, column, line[column:]) for row, line in enumerate(lines) if (column := OPENS[kind](line)) >= 0]
        chosen = comments if wanted is None else named_blocks(comments, lines, wanted)
        after = remove_spans(source, [(row, column, len(lines[row]), "", False) for row, column, _ in chosen])
        return after if proven_lines(kind, source, after) else None
    except (SyntaxError, tokenize.TokenError, ValueError, configparser.Error):
        return None


def strip_sources(cut: Cut, wanted: Wanted) -> None:
    """Every kept text of a kind a strip can prove itself on, stripped; a text of another kind, or one whose strip could not be proven, goes out as written, and a bare cut names it."""
    changed = 0
    carried: Counter[str] = Counter()
    for path in sorted(cut.edition):
        plain = path.endswith(PLAIN) or posixpath.basename(path).startswith(TERMS)
        text = None if path in cut.foreign or plain else as_text(cut.edition[path])
        if text is None:
            continue
        after = stripped(kind_of(path), text, wanted) if kind_of(path) else None
        if after is None:
            carried[posixpath.splitext(path)[1] or posixpath.basename(path)] += 1
        elif after != text:
            cut.edition[path] = after.encode("utf-8")
            changed += 1
    if wanted is not None and changed:
        cut.notes.append(f"{changed} file(s) lost a comment that named the style, each strip proven against its source")
    if wanted is None:
        cut.notes.append(f"{changed} file(s) stripped of comments and docstrings, each strip proven against its source")
        if carried:
            kinds = ", ".join(f"{count} {kind}" for kind, count in sorted(carried.items()))
            cut.notes.append(f"carried as written, since no strip proves itself on their kind: {kinds}")


def style_pattern(cut: Cut, own: list[str]) -> re.Pattern[str]:
    """What names the style in this project, a closed list a machine can decide: the family by its name, a record by its number, and a withheld path by its name."""
    kept_names = {posixpath.basename(path) for path in cut.edition}
    names = {*cut.withheld, *STYLE_FOLDERS, *(entry for entry in own if entry.endswith("/"))}
    names |= {posixpath.basename(path) for path in cut.withheld if path.count("/") <= 1} - kept_names
    paths = "|".join(re.escape(name) for name in sorted(names, key=len, reverse=True))
    return re.compile(rf"My-Styles|(?i:\b(?:decision|record|claim)s? 0\d{{3}}\b)|(?<![\w./-])(?:{paths})(?![\w-])")


def check_silence(cut: Cut, pattern: re.Pattern[str]) -> None:
    """A silent edition names nothing of the style: every kept line that still does is a problem with what it names, and a word the style merely uses is advised."""
    for path in sorted(cut.edition):
        text = None if path in cut.foreign else as_text(cut.edition[path])
        for number, line in enumerate((text or "").splitlines(), 1):
            match = pattern.search(line)
            if match is not None:
                cut.problems.append(
                    f"{path}:{number}: names {match.group(0)!r}, and a silent edition names nothing of the style;"
                    " reword it where it is written, or withhold the file"
                )
            elif (word := VOCABULARY.search(line)) is not None:
                cut.advice.append(f"{path}:{number}: says {word.group(0)!r}, a word of the style's that may also be the product's own")


def take_nested(cut: Cut, nest: str) -> None:
    """A project kept inside this one, cut by its own tool at the same tier and version and laid in at its own path."""
    tool = next((name for name in ("scripts/cut_edition.py", "scripts/cut-edition.mjs") if (ROOT / nest / name).exists()), None)
    if tool is None:
        cut.problems.append(f"{nest}/: carries a guide of its own and no edition tool, so nothing can cut it; give it the tool or withhold it")
        return
    runner = sys.executable if tool.endswith(".py") else "node"
    with tempfile.TemporaryDirectory(prefix="edition-") as scratch:
        target = Path(scratch) / "cut"
        asked = [runner, tool, cut.tier, str(target), "--nested", *(["--silent"] if cut.silent else [])]
        # The nested tool is this project's own tracked file and the arguments are this script's constants.
        done = subprocess.run(asked, cwd=ROOT / nest, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
        said = [line for line in done.stdout.splitlines() if line.strip()]
        if done.returncode != 0:
            cut.problems.extend(f"{nest}/{line}" for line in said[:-1] or [done.stderr.strip() or "its tool said nothing"])
            return
        for path in sorted(found for found in target.rglob("*") if found.is_file()):
            name = f"{nest}/{path.relative_to(target).as_posix()}"
            cut.edition[name] = path.read_bytes()
            cut.foreign.add(name)
        cut.notes.extend(f"{nest}/: {line.strip()}" for line in said[1:])


def laid_overlay(cut: Cut, paths: list[str]) -> dict[str, bytes]:
    """The files the public receives in another form, each at the path it replaces; a nested project leaves its workflow behind, since a workflow is read at a repository's root and nowhere else."""
    chosen = [path for path in paths if path.startswith(OVERLAY)]
    if cut.nested:
        chosen = [path for path in chosen if not path.startswith(f"{OVERLAY}.github/")]
    found = blobs(chosen)
    if found:
        cut.notes.append(f"{len(found)} file(s) laid over the cut from {OVERLAY}")
    return {path[len(OVERLAY) :]: data for path, data in found.items()}


def assemble(cut: Cut) -> None:
    """The edition whole, in memory: what the tier keeps, each nested project by its own tool, the documents rewritten, the sources stripped where the tier or the version asks, and the overlay on top."""
    paths = tracked()
    if cut.tier == "snapshot":
        cut.edition = blobs(paths)
        return
    own = project_list(paths)
    cut.withheld = [path for path in paths if is_withheld(path, own)]
    kept = [path for path in paths if not is_withheld(path, own)]
    nests = nested_roots(kept)
    cut.edition = blobs([path for path in kept if not path.startswith(tuple(f"{nest}/" for nest in nests))])
    for nest in nests:
        take_nested(cut, nest)
    overlay = laid_overlay(cut, paths) if cut.tier == "hand-made" else {}
    rewrite_documents(cut, set(cut.edition) | set(overlay))
    pattern = style_pattern(cut, own)
    if cut.tier == "bare":
        strip_sources(cut, None)
    elif cut.silent:
        strip_sources(cut, lambda text: pattern.search(text) is not None)
    cut.edition.update(overlay)
    if cut.silent:
        check_silence(cut, pattern)
    if not cut.nested and "LICENSE" not in cut.edition:
        cut.advice.append("no LICENSE at the edition's root; a public repository states its terms, and that file is the owner's to add")


def refusal(destination: Path) -> str:
    """Why a cut cannot start, or the empty string: an edition is written outside the repository, into a folder that holds nothing, from a tree every change of which a commit holds."""
    top = Path(git("rev-parse", "--show-toplevel").decode("utf-8").strip() or ROOT).resolve()
    target = destination.resolve()
    if target == top or top in target.parents or target in top.parents:
        return "the destination lies inside the repository or holds it; an edition is written outside"
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        return "the destination exists and is not an empty folder; a cut never writes over anything"
    if git("status", "--porcelain", "--untracked-files=no", "--", ".").strip():
        return "the tree holds changes no commit has; an edition is cut from the last commit, so commit them or put them away first"
    return ""


def overlong(destination: Path, paths: list[str], limit: int = PATH_LIMIT) -> str:
    """Why a destination cannot hold these paths, or the empty string: a path past what the system writes would stop the cut halfway, and a cut is whole or it is nothing."""
    longest = max(paths, key=len, default="")
    length = len(str(destination.resolve())) + 1 + len(longest)
    if length < limit:
        return ""
    return f"under this destination {longest} would run to {length} characters, past the {limit} this system is sure to write; cut into a folder with a shorter path"


def report(cut: Cut, destination: Path) -> None:
    """What a cut did, in the order a reader checks it: what was asked and from which commit, what was written, what was changed on the way, and what is advised."""
    version = "" if cut.tier == "snapshot" else (", silent," if cut.silent else ", attributed,")
    commit = git("rev-parse", "--short=12", "HEAD").decode("utf-8").strip()
    print(f"cut the {cut.tier} edition{version} from {commit} into {destination}")
    print(f"  {len(cut.edition)} file(s) written, {len(cut.withheld)} withheld")
    for note in cut.notes:
        print(f"  {note}")
    if cut.advice and not cut.nested:
        print(f"advisory, {len(cut.advice)} item(s), decides nothing and gates nothing:")
        for item in cut.advice:
            print(f"  {item}")


def run(tier: str, destination: Path, silent: bool, nested: bool) -> int:
    """One cut, written only when it is whole and has no problem to report."""
    stop = refusal(destination)
    if stop:
        print(stop)
        return 1
    cut = Cut(tier, silent, nested)
    assemble(cut)
    stop = overlong(destination, list(cut.edition))
    if stop:
        cut.problems.append(stop)
    if cut.problems:
        for problem in cut.problems:
            print(problem)
        print(f"\n{len(cut.problems)} problem(s). Nothing was written.")
        return 1
    try:
        for path, data in cut.edition.items():
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    except OSError as error:
        print(f"the system stopped the cut while it wrote, so the destination holds a part of it, which is the owner's to remove: {error}")
        return 1
    report(cut, destination)
    return 0


def main() -> int:
    """Cut an edition, or prove the tool."""
    flags = {arg for arg in sys.argv[1:] if arg.startswith("--")}
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if "--selftest" in flags:
        return selftest()
    unknown = flags - {"--silent", "--nested"}
    if len(args) != 2 or args[0] not in TIERS or unknown or (args[0] == "snapshot" and "--silent" in flags):
        print(USAGE)
        return 2
    return run(args[0], Path(args[1]), "--silent" in flags, "--nested" in flags)


# The selftest's project, small enough to read whole: a README by the schema with the sentence that names the family,
# a manifest and a module whose comments name the style in one block and not in another, a workflow the style runs
# and the plain one the public receives, a path the project withholds, and a project nested inside with its own guide.
QUOTES = '"' * 3


def page(*lines: str) -> str:
    """Lines as one text, the way a fixture is easiest to read."""
    return "\n".join(lines)


FIXTURE_README = page(
    "# Sample",
    "",
    "A sample package.",
    "",
    "Sample does one thing. Built from [Keel](https://example.invalid/My-Styles/tree/main/Keel), the package template of the My-Styles family. It is small.",
    "",
    "---",
    "",
    "## Core Architectural Pillars",
    "",
    "1. **One rule.** The core imports nothing outward, as [the reasoning says](docs/decisions/0001-keep-the-core-pure.md).",
    "",
    "---",
    "",
    "## Project Structure",
    "",
    "```text",
    "sample/",
    "├── src/",
    "│   └── sample/                 # The package",
    "├── tests/                      # The suite",
    "├── pyproject.toml              # The manifest",
    "├── AGENTS.md                   # The guide",
    "└── docs/                       # The documents",
    "    └── decisions/              # The reasons",
    "```",
    "",
    "---",
    "",
    "## Getting Started",
    "",
    "```bash",
    "# Install the package",
    "pip install -e .",
    "```",
    "",
    "---",
    "",
    "## Conventions",
    "",
    "The project's conventions live in the rulebook, [docs/CONVENTIONS.md](docs/CONVENTIONS.md).",
    "",
    "---",
    "",
    "## License",
    "",
    "This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.",
    "",
)
FIXTURE_MODULE = page(
    f"{QUOTES}The sample package.{QUOTES}",
    "",
    "import os  # the standard library",
    "",
    "",
    "# Keel's decision 0001 keeps this pure.",
    "# It imports nothing outward.",
    "def double(value: int) -> int:",
    f"    {QUOTES}Twice the value.{QUOTES}",
    "    return value * 2  # type: ignore[no-any-return]  # the checker cannot see it",
    "",
    "",
    "class Port:",
    f"    {QUOTES}A port with nothing in it.{QUOTES}",
    "",
    "",
    "def name() -> str:",
    f"    {QUOTES}The name, with a hash # inside.{QUOTES}",
    '    text = "# not a comment"',
    "    return text + os.sep",
    "",
)
FIXTURE_MANIFEST = page(
    "[project]",
    'name = "sample"  # the name it installs under',
    'version = "0.1.0"',
    'description = "A sample # not a comment"',
    "",
    "# The lint settings are the style's, as AGENTS.md says.",
    "# They change with it.",
    "[tool.sample]",
    "strict = true",
    "",
)
FIXTURE = {
    "AGENTS.md": "# Sample Agent Guide\n\nThe guide.\n",
    "STATE.md": "# State\n\n- Nothing in flight.\n",
    ".codespellignore": "sampleword\n",
    "LICENSE": "The terms.\n",
    "Dockerfile": "# The image\nFROM scratch\n",
    ".gitignore": "# Second working trees, as STATE.md records\n.worktrees/\n\n# caches\n__pycache__/\n",
    ".github/workflows/ci.yml": "name: gate\n",
    "docs/CONVENTIONS.md": "# Conventions\n\nThe rulebook.\n",
    "docs/decisions/0001-keep-the-core-pure.md": "# 0001. Keep the core pure\n",
    "edition/withheld.txt": "# what this project keeps back\nnotes/\n",
    "edition/overlay/.github/workflows/ci.yml": "name: plain\n",
    "notes/private.txt": "kept back\n",
    "scripts/audit_docs.py": "VALUE = 1\n",
    "tests/test_sample.py": "# the suite\nfrom sample import double\n\nVALUE = double(2)\n",
    "pyproject.toml": FIXTURE_MANIFEST,
    "src/sample/__init__.py": FIXTURE_MODULE,
    "README.md": FIXTURE_README,
    "arrows/inner/AGENTS.md": "# Inner Agent Guide\n",
    "arrows/inner/README.md": "# Inner\n\nAn inner project.\n\n## Conventions\n\nSee [the guide](AGENTS.md).\n",
    "arrows/inner/docs/NOTES.md": "# Notes\n",
    "arrows/inner/src/inner.py": f"{QUOTES}Inner.{QUOTES}\n\nVALUE = 1  # one\n",
    "arrows/inner/edition/overlay/.github/workflows/ci.yml": "name: inner\n",
    "arrows/inner/edition/overlay/CONTRIBUTING.md": "# Contributing\n",
}
# What a second project adds to be refused: a docstring that names the style, an image the edition cannot show, and
# a nested project with no tool of its own to cut it.
FIXTURE_TOLD = {
    "src/sample/told.py": f"{QUOTES}As AGENTS.md says.{QUOTES}\n",
    "docs/map.png": "not a picture\n",
    "README.md": FIXTURE_README.replace("A sample package.", "A sample package.\n\n![The map](docs/map.png)"),
}


def fixture_git(root: Path, *args: str) -> None:
    """One git call in a fixture's tree, which must succeed."""
    # The arguments are this script's own constants and git is the tool the family runs on.
    subprocess.run(["git", *args], cwd=root, capture_output=True, check=True)  # noqa: S603, S607


def build_fixture(root: Path, files: dict[str, str], nested_tool: bool) -> None:
    """A committed project in a scratch folder, with this tool at its own path and, where asked, in the project nested inside."""
    homes = ["scripts/cut_edition.py", *(["arrows/inner/scripts/cut_edition.py"] if nested_tool else [])]
    contents = {path: text.encode("utf-8") for path, text in files.items()} | dict.fromkeys(homes, Path(__file__).read_bytes())
    for path, data in contents.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    fixture_git(root, "init", "-q")
    fixture_git(root, "config", "core.autocrlf", "false")
    fixture_git(root, "add", "-A")
    fixture_git(root, "-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture")


def cut_fixture(root: Path, out: Path, *args: str) -> tuple[int, str, dict[str, str]]:
    """One cut of a fixture by its own copy of this tool: how it ended, what it said, and what it wrote."""
    asked = [sys.executable, "scripts/cut_edition.py", args[0], str(out), *args[1:]]
    # The tool run is the fixture's copy of this file and the arguments are this script's constants.
    done = subprocess.run(asked, cwd=root, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
    found = sorted(path for path in out.rglob("*") if path.is_file()) if out.exists() else []
    return done.returncode, done.stdout, {path.relative_to(out).as_posix(): path.read_bytes().decode("utf-8") for path in found}


def expect(holds: bool, what: str) -> int:
    """One failure counted and named, or none."""
    if not holds:
        print(f"WRONG: {what}")
    return 0 if holds else 1


def prove_snapshot(root: Path, out: Path) -> int:
    """The snapshot is every tracked file as it stands, the workshop's own among them."""
    code, _, files = cut_fixture(root, out, "snapshot")
    everything = [path for path in ("AGENTS.md", "docs/CONVENTIONS.md", "notes/private.txt", "arrows/inner/AGENTS.md", "scripts/cut_edition.py") if path in files]
    failures = expect(code == 0 and len(everything) == 5, "the snapshot left out a tracked file")
    return failures + expect(files.get("src/sample/__init__.py") == FIXTURE_MODULE, "the snapshot changed a file it carried")


def prove_hand_made(root: Path, out: Path) -> int:
    """The hand-made tier withholds the workshop, carries the code as written, lays the overlay, and rewrites the README for what it holds."""
    code, _, files = cut_fixture(root, out, "hand-made")
    readme = files.get("README.md", "")
    held = [path for path in files if path.startswith(("docs/", "edition/", "notes/")) or path.endswith(("AGENTS.md", "STATE.md", "audit_docs.py", "cut_edition.py", ".codespellignore"))]
    failures = expect(code == 0 and not held, f"the hand-made tier carried what it withholds: {held}")
    failures += expect(files.get(".github/workflows/ci.yml") == "name: plain\n", "the overlay's workflow did not replace the style's")
    failures += expect(files.get("src/sample/__init__.py") == FIXTURE_MODULE, "the hand-made tier changed code it carries as written")
    failures += expect("## Conventions" not in readme and "docs/" not in readme, "the README kept its Conventions section or a withheld path")
    failures += expect("as the reasoning says." in readme, "a link into a withheld path was not turned back into its words")
    failures += expect("└── pyproject.toml" in readme and "AGENTS.md" not in readme, "a drawn tree kept a withheld entry or left its last branch open")
    failures += expect(NOTICES["hand-made"] in readme and "Built from [Keel]" in readme, "the attributed README lost its notice or its attribution")
    failures += expect("arrows/inner/src/inner.py" in files and "arrows/inner/AGENTS.md" not in files, "the nested project was not cut by its own tool")
    failures += expect("arrows/inner/CONTRIBUTING.md" in files, "the nested project's overlay was not laid")
    return failures + expect("arrows/inner/.github/workflows/ci.yml" not in files, "a nested project carried a workflow no root reads")


def prove_silent(root: Path, out: Path) -> int:
    """The silent version drops a comment that names the style, cuts the sentence that names the family, and keeps every other word."""
    code, said, files = cut_fixture(root, out, "hand-made", "--silent")
    readme, module = files.get("README.md", ""), files.get("src/sample/__init__.py", "")
    failures = expect(code == 0, f"the silent cut of a project that can be silent was refused:\n{said}")
    failures += expect("My-Styles" not in readme and NOTICES["hand-made"] not in readme, "the silent README names the family or carries the notice")
    failures += expect("Sample does one thing. It is small." in readme, "the silent README lost a sentence that named nothing")
    failures += expect("keeps this pure" not in module and "imports nothing outward" not in module, "a comment block that names the style was not dropped whole")
    failures += expect("# the standard library" in module and "Twice the value." in module, "the silent cut dropped a comment or a docstring that named nothing")
    failures += expect("AGENTS.md" not in files.get("pyproject.toml", "") and "the name it installs under" in files.get("pyproject.toml", ""), "the manifest's comments were not sorted by what they name")
    failures += expect("STATE.md" not in files.get(".gitignore", "") and "# caches" in files.get(".gitignore", ""), "the ignore file's comments were not sorted by what they name")
    return failures + expect("cut for naming the family" in said, "the cut did not report the sentence it took")


def prove_bare(root: Path, out: Path) -> int:
    """The bare tier strips every comment and docstring a proof covers, keeps what instructs a tool, and cuts the README to what the thing is and how to run it."""
    code, said, files = cut_fixture(root, out, "bare")
    readme, module, manifest = files.get("README.md", ""), files.get("src/sample/__init__.py", ""), files.get("pyproject.toml", "")
    failures = expect(code == 0 and QUOTES not in module and "standard library" not in module, "the bare tier left a docstring or a comment in a module")
    failures += expect("# type: ignore[no-any-return]" in module and "cannot see it" not in module, "an instruction to a tool was dropped, or the reason after it kept")
    failures += expect('"# not a comment"' in module and "class Port:\n    ...\n" in module, "a string was cut as a comment, or a body left empty")
    failures += expect('"A sample # not a comment"' in manifest and manifest.count("#") == 1, "the manifest kept a comment or lost a hash inside a string")
    failures += expect("## Getting Started" in readme and "## License" in readme and "## Project Structure" not in readme, "the bare README is not its opening, how to run it and its terms")
    failures += expect(NOTICES["bare"] in readme, "the bare README lost its notice")
    failures += expect(".github/workflows/ci.yml" not in files and "arrows/inner/CONTRIBUTING.md" not in files, "the bare tier took the overlay")
    failures += expect(files.get("Dockerfile") == FIXTURE["Dockerfile"] and "Dockerfile" in said, "a kind no strip proves itself on was changed or went unnamed")
    return failures + expect(QUOTES not in files.get("arrows/inner/src/inner.py", QUOTES), "the nested project was not stripped by its own tool")


def prove_refusals(root: Path, told: Path, out: Path) -> int:
    """A cut that cannot be whole writes nothing: a destination inside the repository or already holding something, a tree with uncommitted changes, a version the tier has not, and a silent edition that still names the style."""
    failures = expect(cut_fixture(root, root / "inside", "hand-made")[0] == 1, "a destination inside the repository was accepted")
    full = out / "full"
    full.mkdir(parents=True)
    (full / "kept.txt").write_text("already here\n", encoding="utf-8")
    failures += expect(cut_fixture(root, full, "hand-made")[0] == 1 and (full / "kept.txt").exists(), "a destination that holds something was written over")
    failures += expect(cut_fixture(root, out / "usage", "snapshot", "--silent")[0] == 2, "the snapshot was offered a silent version")
    (root / "LICENSE").write_text("changed\n", encoding="utf-8")
    failures += expect(cut_fixture(root, out / "dirty", "hand-made")[0] == 1, "a tree with uncommitted changes was cut")
    fixture_git(root, "checkout", "--", "LICENSE")
    code, said, files = cut_fixture(told, out / "told", "hand-made", "--silent")
    failures += expect(code == 1 and not files and "Nothing was written." in said, "a silent cut that still names the style wrote something")
    failures += expect("src/sample/told.py:1: names 'AGENTS.md'" in said, "a docstring that names the style did not refuse the silent cut")
    failures += expect("the image docs/map.png is not in the edition" in said, "an image the edition cannot show raised nothing")
    return failures + expect("arrows/inner/: carries a guide of its own and no edition tool" in said, "a nested project with no tool was passed over")


def prove_strips() -> int:
    """A strip is trusted only through its proof: a text changed beyond its comments is refused, and a comment the line reader cannot place is left where it is."""
    failures = expect(not proven_python("x = 1  # c\n", "x = 2\n", None), "the proof passed a strip that changed a value")
    failures += expect(proven_python("x = 1  # c\n", "x = 1\n", None), "the proof refused a strip that took a comment alone")
    failures += expect(stripped("toml", f"a = {QUOTES}\n# inside the string\n{QUOTES}\n", None) is None, "a line inside a string was cut as a comment and the proof did not catch it")
    failures += expect(stripped("ini", "[a]\n; note\nb = 1\n", None) == "[a]\nb = 1\n", "an INI comment was not stripped")
    failures += expect(overlong(Path("d"), ["a.txt"], limit=1) != "" and not overlong(Path("d"), ["a.txt"], limit=10**6), "a destination whose paths the system cannot write was not refused before the cut wrote")
    return failures + expect(stripped("edge", "# note\n  # a pattern, not a comment\nbuild/\n", None) == "  # a pattern, not a comment\nbuild/\n", "an ignore file lost a line that was no comment")


def selftest() -> int:
    """Prove the tool on a project of its own making, since a cut that was never checked against what it should hold proves nothing."""
    with tempfile.TemporaryDirectory(prefix="edition-selftest-") as scratch:
        root, told, out = Path(scratch) / "project", Path(scratch) / "told", Path(scratch) / "out"
        build_fixture(root, FIXTURE, nested_tool=True)
        build_fixture(told, FIXTURE | FIXTURE_TOLD, nested_tool=False)
        failures = prove_snapshot(root, out / "snapshot") + prove_hand_made(root, out / "hand-made")
        failures += prove_silent(root, out / "silent") + prove_bare(root, out / "bare")
        failures += prove_refusals(root, told, out) + prove_strips()
    if failures:
        print(f"\n{failures} proof(s) failed. The tool does not cut what its law says.")
        return 1
    print("every cut holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
