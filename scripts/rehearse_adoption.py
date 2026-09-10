"""Build a child from each template, shaped the way adoption shapes it, and run the child's gate.

A check proven only in the template is proven where its preconditions are absent: the template
carries no inherited folder, no upstream file, its own records from 0001, files written with bare
line feeds, and no commit older than the rule under test. A project built from it has the opposite
of every one of those, so this script builds one per seat in a temporary repository and requires
its docs audit to pass, its selftest where it has one to report every rule firing, and its tree to
be unchanged afterwards. The family workflow runs it on every change.
"""

import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Seat folder, audit command, selftest command or None, and the style's name for the child's prose.
SEATS: list[tuple[str, list[str], list[str] | None, str]] = [
    ("ArchtypeCore", [sys.executable, "scripts/audit_docs.py"], None, "ArchetypeCore"),
    ("Keel", [sys.executable, "scripts/audit_docs.py"], None, "Keel"),
    ("Helm", ["node", "scripts/audit-docs.mjs"], None, "Helm"),
    (
        "Quiver",
        [sys.executable, "scripts/audit_inquiry.py"],
        [sys.executable, "scripts/audit_inquiry.py", "--selftest"],
        "Quiver",
    ),
]
# What a copy of a seat leaves behind: nothing tracked lives in these.
UNTRACKED_CLUTTER = (".git", "node_modules", "__pycache__", ".hypothesis", "dist", ".mypy_cache", ".ruff_cache", ".pytest_cache")
LONG_TITLE = "a-record-whose-title-runs-well-past-the-cap-of-seventy-two-characters"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """One command in one directory, its output kept for the report."""
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, shell=False)


def git(cwd: Path, *args: str) -> str:
    """One git call in the child, which must succeed."""
    done = run(["git", *args], cwd)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {done.stderr.strip()}")
    return done.stdout.strip()


def record_text(number: str, title: str, today: str) -> str:
    """A decision record of the family's shape."""
    return (
        f"# {number}. {title}\n\nStatus: Accepted\nDate: {today}\n\n"
        "## Context\n\nThe rehearsal needed a record of this project's own.\n\n"
        "## Decision\n\nIt has one.\n\n"
        "## Consequences\n\nThe checks that read the project's own records have something to read.\n"
    )


def shape_child(child: Path, style: str, pin: str, today: str) -> None:
    """Give the copy the shape adoption gives a project."""
    decisions = child / "docs/decisions"
    inherited = child / "docs/inherited"
    inherited.mkdir()
    numbers: list[int] = []
    for record in sorted(decisions.glob("*.md")):
        numbers.append(int(record.name[:4]))
        record.rename(inherited / record.name)
    # The project's own records continue after the inherited ones, the shape a project that kept
    # its numbers has, so no record numbered 0001 is the project's own.
    own = max(numbers) + 1
    own_record = decisions / f"{own:04d}-adopt-the-style-as-this-project-s-law.md"
    own_record.write_text(record_text(f"{own:04d}", f"Adopt the {style} style as this project's law", today), encoding="utf-8")
    # A long-named record committed before the audit arrives; the cap must leave it alone.
    long_record = decisions / f"{own + 1:04d}-{LONG_TITLE}.md"
    long_record.write_text(record_text(f"{own + 1:04d}", "A record from before the cap arrived", today), encoding="utf-8")
    (child / "docs/UPSTREAM.md").write_text(
        "# Upstream\n\n"
        f"Aligned to {style} at `{pin}`.\n\n"
        "Every entry below is a lead, not a verdict; verify it against the template's own tree before adopting it.\n\n"
        "## Open\n\n"
        f"### {today} A rehearsed entry with every part in place\n\n"
        "Kind: improvement\n"
        f"Pin: {pin}\n\n"
        "**What it is.** An entry the rehearsal writes so the schema check has one to read.\n\n"
        "**How the work surfaced it.** Building this child.\n\n"
        "**Why it is believed better.** It exercises the shape a project's first entry takes.\n\n"
        "**Records checked.** None rules on it.\n",
        encoding="utf-8",
    )
    agents = child / "AGENTS.md"
    lines = agents.read_text(encoding="utf-8").split("\n")
    anchor = next(i for i, line in enumerate(lines) if line.startswith("| [docs/decisions/](docs/decisions/)"))
    lines[anchor + 1:anchor + 1] = [
        f"| [docs/inherited/](docs/inherited/) | {style}'s decision records, carried whole and byte-identical at the pin. Never edited here. |",
        "| [docs/UPSTREAM.md](docs/UPSTREAM.md) | What this project has for its style, each an entry until re-alignment resolves it. |",
    ]
    agents.write_text("\n".join(lines), encoding="utf-8")
    # The map and the README point at records that now live in the inherited folder.
    for rel in ("README.md", "docs/ARCHITECTURE.md"):
        doc = child / rel
        text = doc.read_text(encoding="utf-8")
        doc.write_text(text.replace("docs/decisions/0", "docs/inherited/0").replace("](decisions/0", "](inherited/0"), encoding="utf-8")
    state = child / "STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace("- Nothing deferred.", f"- A rehearsed deferral, verified today ({today}).", 1),
        encoding="utf-8",
    )


def strip_demo_inquiry(child: Path, today: str) -> None:
    """Take the host's demo out, the way a project built from it does before writing its own inquiry.

    The demo's claims pin commits of the template's history, which a project does not have, and
    its arrow, manifest, and review pass are replaceable examples; a fresh inquiry starts with one
    conjecture, no arrow, and no pass, and its living documents stop pointing at the demo.
    """
    shutil.rmtree(child / "arrows")
    shutil.rmtree(child / "docs/arrows")
    shutil.rmtree(child / "docs/reviews")
    for claim in (child / "docs/claims").glob("*.md"):
        claim.unlink()
    (child / "docs/claims/0001-a-rehearsed-conjecture.md").write_text(
        f"# 0001. A rehearsed conjecture\n\nStatus: Conjecture\nDate: {today}\n\n"
        "## Claim\n\nThe rehearsal's first conjecture, which must convince nobody yet.\n\n"
        "## Evidence\n\nNone.\n\n## Threats\n\n- None named.\n",
        encoding="utf-8",
    )
    agents = child / "AGENTS.md"
    kept = [
        line for line in agents.read_text(encoding="utf-8").split("\n")
        if not line.startswith(("| [arrows/coinwise/README.md]", "| [docs/arrows/]", "| [docs/reviews/]"))
    ]
    kept = [
        "- Work on an arrow: use that arrow's own commands, stated in its README." if line.startswith("- Work on an arrow:") else line
        for line in kept
    ]
    agents.write_text("\n".join(kept), encoding="utf-8")
    readme = child / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("([coinwise](arrows/coinwise/))", "(the demo arrow)"), encoding="utf-8")
    (child / "docs/QUESTION.md").write_text(
        "# The Question\n\n"
        "What a rehearsed inquiry asks, bounded to what this child can answer.\n\n"
        "## The decomposition\n\n"
        "- Open. The first conjecture stands in [claim 0001](claims/0001-a-rehearsed-conjecture.md), unbacked until an arrow exists.\n",
        encoding="utf-8",
    )
    architecture = child / "docs/ARCHITECTURE.md"
    lines = [
        line.replace("[coinwise](arrows/coinwise.md)", "coinwise")
        for line in architecture.read_text(encoding="utf-8").split("\n")
        if not line.startswith(("- A settled claim", "- A superseded claim", "- An arrow manifest", "- A review pass record"))
    ]
    architecture.write_text("\n".join(lines), encoding="utf-8")


def build_history(child: Path) -> None:
    """Two commits, the audit arriving in the second, then a checkout with Windows line endings."""
    git(child, "init", "-q")
    git(child, "config", "user.email", "rehearsal@example.invalid")
    git(child, "config", "user.name", "Rehearsal")
    git(child, "config", "core.longpaths", "true")
    git(child, "add", "-A", "--", ".", ":!scripts")
    git(child, "commit", "-q", "-m", "Adopt the style, records and all, before its audit arrives")
    git(child, "add", "-A")
    git(child, "commit", "-q", "-m", "The audit arrives")
    git(child, "config", "core.autocrlf", "true")
    git(child, "rm", "-r", "-q", "--cached", ".")
    git(child, "reset", "-q", "--hard")


def rehearse(seat: str, audit: list[str], selftest: list[str] | None, style: str, pin: str, workspace: Path) -> list[str]:
    """Every way the child's gate disagreed with the rehearsal, empty when it agreed."""
    child = workspace / seat
    shutil.copytree(ROOT / seat, child, ignore=shutil.ignore_patterns(*UNTRACKED_CLUTTER))
    today = datetime.now(UTC).date().isoformat()
    if seat == "Quiver":
        strip_demo_inquiry(child, today)
    shape_child(child, style, pin, today)
    build_history(child)
    findings: list[str] = []
    audited = run(audit, child)
    if audited.returncode != 0:
        findings.append(f"{seat}: the child's audit failed:\n{audited.stdout}{audited.stderr}")
    if selftest is not None:
        proven = run(selftest, child)
        if proven.returncode != 0 or "every rule fires" not in proven.stdout:
            findings.append(f"{seat}: the child's selftest did not prove every rule:\n{proven.stdout}{proven.stderr}")
        leftovers = git(child, "status", "--porcelain")
        if leftovers:
            findings.append(f"{seat}: the selftest left the child's tree changed:\n{leftovers}")
    return findings


def main() -> int:
    """Rehearse every seat and report."""
    pin = run(["git", "rev-parse", "--short=12", "HEAD"], ROOT).stdout.strip() or "000000000000"
    findings: list[str] = []
    with tempfile.TemporaryDirectory(prefix="rehearse-", ignore_cleanup_errors=True) as scratch:
        workspace = Path(scratch)
        for seat, audit, selftest, style in SEATS:
            seat_findings = rehearse(seat, audit, selftest, style, pin, workspace)
            findings.extend(seat_findings)
            verdict = "did not pass" if seat_findings else "passed"
            print(f"rehearsed {seat} as a child: its gate {verdict}")
    for finding in findings:
        print(finding)
    if findings:
        print(f"\n{len(findings)} finding(s). A check is green here and red where a project would run it.")
        return 1
    print("Every seat's gate passes in a project shaped by adoption.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
