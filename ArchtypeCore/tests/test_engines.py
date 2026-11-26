import shutil
import subprocess
import sys
from pathlib import Path

# An engine sits beside app with its own suites and ports, as the engines README lays it out, and
# the template carries none, so each case builds one in a scratch folder beside a copy of the
# project's configuration and asks the suite run or the lint what it makes of it.

ROOT = Path(__file__).resolve().parents[1]
ENGINE_SUITE = "def test_the_engine_answers() -> None:\n    assert True\n"
ENGINE_PORT = (
    '"""The demo engine\'s port."""\n\nfrom abc import ABC, abstractmethod\n\n\n'
    'class IDemoPort(ABC):\n\n    """A port the demo engine drives."""\n\n'
    "    @abstractmethod\n    def ping(self) -> str: ...\n"
)


def engine_tree(tmp_path: Path) -> Path:
    shutil.copy(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    (tmp_path / "tests").mkdir()
    suite = tmp_path / "engines" / "demo" / "tests"
    suite.mkdir(parents=True)
    (suite / "test_demo.py").write_text(ENGINE_SUITE, encoding="utf-8")
    ports = tmp_path / "engines" / "demo" / "domain" / "interfaces"
    ports.mkdir(parents=True)
    (ports / "demo_port.py").write_text(ENGINE_PORT, encoding="utf-8")
    return tmp_path


def test_the_suite_run_collects_an_engines_suites(tmp_path: Path) -> None:
    tree = engine_tree(tmp_path)

    collected = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:randomly"],
        cwd=tree,
        capture_output=True,
        text=True,
        check=False,
    )

    assert "engines/demo/tests/test_demo.py::test_the_engine_answers" in collected.stdout


def test_an_engines_suites_and_ports_pass_the_lint_as_the_apps_do(tmp_path: Path) -> None:
    tree = engine_tree(tmp_path)

    linted = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "engines"],
        cwd=tree,
        capture_output=True,
        text=True,
        check=False,
    )

    assert linted.returncode == 0, linted.stdout
