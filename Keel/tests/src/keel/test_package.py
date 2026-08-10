import logging
import os
import subprocess
import sys

# Library citizenship, pinned: the package logger stays silent by default, importing the
# package reads no environment, and the version is the style's fixed 0.0.1.


def test_the_package_logger_carries_a_null_handler() -> None:
    import keel  # noqa: F401

    handlers = logging.getLogger("keel").handlers
    assert any(isinstance(h, logging.NullHandler) for h in handlers)


def test_importing_the_package_needs_no_environment() -> None:
    # A clean interpreter with an emptied environment imports the package or it does not;
    # an import-time environment read would crash right here.
    result = subprocess.run(
        [sys.executable, "-c", "import keel"],
        env={"PATH": os.environ.get("PATH", ""), "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr


def test_the_style_version_is_pinned() -> None:
    import keel

    assert keel.__version__ == "0.0.1"
