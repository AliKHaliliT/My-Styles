"""Audit the treasury's index of the names its studies share, and advise on a colon splice before a record lands.

A study is an immutable record and never cites another study, so a name that
two studies both carry in bold is joined nowhere unless a living file joins it.
The index of shared names is that file: one row per name that two or more
studies' findings carry in bold, with the studies that hold it and one word
saying whether they name the same thing. This script computes the shared names
from the findings files and holds the rows to them. Every shared name has one
row, no row names an unshared name, a row's studies are the studies that hold
its name, the rows stand in alphabetical order, and the meaning cell is one of
two words. Whether the word is the right one stays with review, which is where
the index's own record says it has to stay.

A study's findings are its numbered files after the research record. A bold
name is the text between one pair of double asterisks, joined across a line
break when a line ends inside the pair and never across a blank line, compared
lowercased with its whitespace collapsed and trailing punctuation dropped. A
name of one or two characters is not counted.

The second duty is advice. The prose law bans a colon that splices two clauses and leaves the verdict
to review, because a list colon and a spliced one look alike to a machine. In a treasury record that
main does not hold yet, a colon that closes a clause of three words or more and opens a lowercase one
is printed as advice, and the advice falls silent once the record has landed, since a defect found
in a merged record stays.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREASURY = ROOT / "treasury"
INDEX_NAME = "SHARED-NAMES.md"
INDEX_REL = f"treasury/{INDEX_NAME}"
HEADER = "| Name | Studies | Meaning |"
MEANINGS = ("same", "different")
BOLD = re.compile(r"\*\*([^*]+?)\*\*")
CODE = re.compile(r"`[^`\n]*`")
SPLICE = re.compile(r"(?:^|(?<=[.!?] )|(?<=\*\* ))([^.!?:*]{0,400}?): (?=[a-z])")
RECORD = re.compile(r"treasury/(?:decisions/[^/]+|\d{4}-[^/]+/\d\d-[^/]+)\.md$")


def git(*args: str) -> str:
    """One git call against the repository this file lives in; empty when git says no."""
    # The arguments are this script's own constants and git is the tool the family runs on.
    done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    return done.stdout if done.returncode == 0 else ""


def landing_base() -> str | None:
    """The ref a record counts as landed against: main, or the remote's main where the checkout has no local one."""
    for ref in ("main", "origin/main"):
        if git("rev-parse", "--verify", "--quiet", ref).strip():
            return ref
    return None


def unlanded_records() -> list[str]:
    """Treasury records that main does not hold yet: new or changed in the working tree, or in commits main lacks."""
    paths = set(git("diff", "--name-only", "HEAD").split("\n")) | set(git("ls-files", "--others", "--exclude-standard").split("\n"))
    base = landing_base()
    if base is not None:
        paths |= set(git("log", "--name-only", "--format=", f"{base}..HEAD").split("\n"))
    return sorted(p for p in paths if RECORD.match(p) and (ROOT / p).is_file())


def prose_blocks(text: str) -> list[list[tuple[int, str]]]:
    """The prose of a record as blocks of numbered lines, a block ending at a blank line, a heading, a table row, a fence or a list marker."""
    blocks: list[list[tuple[int, str]]] = []
    fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fence = not fence
        elif fence or not line.strip() or line.startswith(("#", "|", "Status:", "Date:")):
            blocks.append([])
        elif line.startswith(("- ", "* ")) or not blocks:
            blocks.append([(number, line)])
        else:
            blocks[-1].append((number, line))
    return [block for block in blocks if block]


def splice_candidates(text: str) -> list[tuple[int, str]]:
    """Each colon in a record's prose that closes a clause of three words or more and opens a lowercase one, with the colon's line and its clause.

    A block's lines are joined before matching, because a wrapped line can carry the colon while the
    line above carries the clause, and a rule that read one line at a time passed exactly that shape.
    """
    found: list[tuple[int, str]] = []
    for block in prose_blocks(text):
        starts: list[int] = []
        joined = ""
        for _, line in block:
            starts.append(len(joined))
            joined += CODE.sub(" ", line) + " "
        for match in SPLICE.finditer(joined):
            if len(match.group(1).split()) >= 3:
                colon = match.end() - 2
                number = block[max(i for i, start in enumerate(starts) if start <= colon)][0]
                found.append((number, match.group(1).strip()[-40:]))
    return found


def advise_splices(advice: list[str]) -> None:
    """A colon opening a lowercase clause in a treasury record main does not hold yet, advised and never gated."""
    for rel in unlanded_records():
        for number, clause in splice_candidates((ROOT / rel).read_text(encoding="utf-8")):
            advice.append(
                f"{rel}:{number}: the colon after {clause!r} opens a lowercase clause;"
                " a list, a quote or a label keeps its colon, and a spliced clause becomes two sentences"
            )


def findings_files(treasury: Path) -> list[Path]:
    """Every findings file: the numbered files of a study folder after its research record."""
    return sorted(
        path
        for path in treasury.glob("[0-9][0-9][0-9][0-9]-*/[0-9][0-9]-*.md")
        if not path.name.startswith("01-")
    )


def normalized(raw: str) -> str:
    """A bold name as the index compares it."""
    return " ".join(raw.split()).lower().rstrip(".,;:")


def bold_names(text: str) -> set[str]:
    """The normalized bold names in a text, a name wrapped across a line break included."""
    names: set[str] = set()
    pending = ""
    for line in [*text.splitlines(), ""]:
        pending = f"{pending} {line.strip()}" if pending else line
        if line.strip() and pending.count("**") % 2:
            continue
        names.update(normalized(match.group(1)) for match in BOLD.finditer(pending))
        pending = ""
    return {name for name in names if len(name) > 2}


def shared_names(treasury: Path) -> dict[str, list[str]]:
    """Every name that two or more studies carry in bold, with the studies that hold it."""
    holders: dict[str, set[str]] = {}
    for path in findings_files(treasury):
        for name in bold_names(path.read_text(encoding="utf-8")):
            holders.setdefault(name, set()).add(path.parent.name[:4])
    return {name: sorted(studies) for name, studies in holders.items() if len(studies) > 1}


def index_rows(text: str) -> list[tuple[int, list[str]]] | None:
    """The rows of the index table as (line number, cells), or None when the header is missing."""
    lines = text.splitlines()
    if HEADER not in lines:
        return None
    start = lines.index(HEADER) + 2
    rows: list[tuple[int, list[str]]] = []
    for number, line in enumerate(lines[start:], start + 1):
        if not line.startswith("|"):
            break
        rows.append((number, [cell.strip() for cell in line.strip().strip("|").split("|")]))
    return rows


def render_row(name: str, studies: list[str], meaning: str) -> str:
    """One row of the index."""
    return f"| {name} | {', '.join(studies)} | {meaning} |"


def check_row(number: int, cells: list[str], shared: dict[str, list[str]], problems: list[str]) -> None:
    """A row names a shared name, its holders, and one of the two words."""
    if len(cells) != 3:
        problems.append(f"{INDEX_REL}:{number} has {len(cells)} cells; a row is name, studies, meaning")
        return
    name, studies, meaning = cells
    if name not in shared:
        problems.append(f"{INDEX_REL}:{number} lists `{name}`, which no two studies carry in bold; delete the row")
    elif studies != ", ".join(shared[name]):
        problems.append(
            f"{INDEX_REL}:{number} says `{name}` is held by {studies}; the findings say {', '.join(shared[name])}"
        )
    if meaning not in MEANINGS:
        problems.append(
            f"{INDEX_REL}:{number} gives `{name}` the meaning {meaning!r};"
            " read every holder's entry and write same or different"
        )


def check_index(rows: list[tuple[int, list[str]]] | None, shared: dict[str, list[str]], problems: list[str]) -> None:
    """Every shared name has one row, no row is stale, and the rows stand in alphabetical order."""
    if rows is None:
        problems.append(f"{INDEX_REL} lacks the table header {HEADER}")
        return
    seen: dict[str, int] = {}
    for number, cells in rows:
        check_row(number, cells, shared, problems)
        if cells[0] in seen:
            problems.append(f"{INDEX_REL}:{number} repeats `{cells[0]}`, first listed at line {seen[cells[0]]}")
        seen.setdefault(cells[0], number)
    names = [cells[0] for _, cells in rows]
    if names != sorted(names):
        problems.append(f"{INDEX_REL} lists its rows out of alphabetical order")
    for name in sorted(shared.keys() - seen.keys()):
        problems.append(
            f"{INDEX_REL} lacks a row for `{name}`; add `{render_row(name, shared[name], 'same or different')}`"
            " and read every holder's entry to choose the word"
        )


def run(treasury: Path) -> tuple[list[str], list[str], int]:
    """Every problem in the index of shared names, every piece of advice, and the count of shared names."""
    shared = shared_names(treasury)
    advice: list[str] = []
    advise_splices(advice)
    index = treasury / INDEX_NAME
    if not index.exists():
        return [f"{INDEX_REL} is missing; the treasury indexes every name its studies share"], advice, len(shared)
    problems: list[str] = []
    check_index(index_rows(index.read_text(encoding="utf-8")), shared, problems)
    return problems, advice, len(shared)


def expect(problems: list[str], needle: str, what: str) -> int:
    """One failure when no problem carries the needle."""
    if any(needle in problem for problem in problems):
        return 0
    print(f"WRONG: {what} raised nothing carrying {needle!r}")
    return 1


def judged(text: str, shared: dict[str, list[str]]) -> list[str]:
    """The problems an index text raises against the given shared names."""
    problems: list[str] = []
    check_index(index_rows(text), shared, problems)
    return problems


def prove_reader() -> int:
    """The bold reader joins a wrap, drops a short name and trailing punctuation, and stops at a blank line."""
    sample = "a **wrapped\nname** here, **it** and **two.**\n\n**open\n\n**closed**"
    if bold_names(sample) == {"wrapped name", "two", "closed"}:
        return 0
    print("WRONG: the bold reader mishandles a wrap, a short name, trailing punctuation or an unpaired marker")
    return 1


def prove_splice_advice() -> int:
    """A spliced clause in a treasury record main does not hold is advised once, the label and the list intro beside it are not, and the record leaves."""
    record = TREASURY / "decisions" / "9900-planted-splice.md"
    record.write_text(
        "# 9900. Planted splice\n\nStatus: Accepted\nDate: 2026-01-01\n\n## Context\n\n"
        "The reader found the second defect, which is why: the dot was gone.\n"
        "- **A label.** Rejected: it duplicates what the tree records.\n"
        "The audit gains three checks:\n\n"
        "Reproduced in a fresh environment with the seat's development\n"
        "requirements: the revealed type was nothing.\n",
        encoding="utf-8",
    )
    try:
        found = [a for a in run(TREASURY)[1] if record.name in a and "lowercase clause" in a]
        if len(found) == 2 and f"{record.name}:8:" in found[0] and f"{record.name}:13:" in found[1]:
            return 0
        print(f"WRONG: the planted splices were advised {len(found)} time(s) instead of once each at lines 8 and 13, {found}")
        return 1
    finally:
        record.unlink()


def selftest() -> int:
    """Every check fires on a planted defect and stays silent on a sound index."""
    failures = prove_reader() + prove_splice_advice()
    shared = shared_names(TREASURY)
    if len(shared) < 2:
        print("WRONG: fewer than two shared names in the treasury; the plants need two rows")
        return failures + 1
    rows = [render_row(name, shared[name], "same") for name in sorted(shared)]
    head = [HEADER, "| --- | --- | --- |"]
    sound = judged("\n".join(head + rows), shared)
    if sound:
        failures += 1
        print(f"WRONG: a sound index raised {sound}")
    wrong_studies = render_row(min(shared), ["0001", "0002", "0003", "0004", "0005"], "same")
    plants = [
        (head + rows[1:], "lacks a row for", "a missing row"),
        (head + rows[1:] + rows[:1], "alphabetical order", "a misplaced row"),
        (head + rows + [rows[0]], "repeats", "a repeated row"),
        (head + rows + [render_row("zz planted name", ["0001", "0002"], "same")], "no two studies carry", "a stale row"),
        (head + [wrong_studies] + rows[1:], "the findings say", "a wrong studies cell"),
        (head + [rows[0].replace("| same |", "| unread |")] + rows[1:], "same or different", "a third word"),
        (head + ["| only two cells |"] + rows[1:], "cells", "a short row"),
        (rows, "lacks the table header", "a missing header"),
    ]
    for lines, needle, what in plants:
        failures += expect(judged("\n".join(lines), shared), needle, what)
    if failures == 0:
        print("The treasury audit's checks fire on every planted defect and pass a sound index.")
    return failures


def main() -> int:
    """Hold the index of shared names to the findings, or prove the checks when asked."""
    if "--selftest" in sys.argv[1:]:
        return selftest()
    problems, advice, count = run(TREASURY)
    for problem in problems:
        print(problem)
    if advice:
        print(f"advisory, {len(advice)} item(s), decides nothing and gates nothing:")
        for line in advice:
            print(f"  {line}")
    if problems:
        print(f"\n{len(problems)} problem(s). The index of shared names does not match the findings.")
        return 1
    print(f"The index of shared names matches the findings: {count} names held by more than one study.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
