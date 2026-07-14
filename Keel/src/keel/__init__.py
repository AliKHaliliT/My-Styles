from importlib.metadata import PackageNotFoundError, version
from logging import NullHandler, getLogger

from keel.core.config import EngineConfig
from keel.core.logging import PACKAGE_LOGGER_NAME
from keel.facade.engine import Engine, EngineBuilder
from keel.facade.schemas import RunReport, RunRequest, StepReport

try:
    __version__ = version("keel")
except PackageNotFoundError:
    __version__ = "0.0.0"

getLogger(PACKAGE_LOGGER_NAME).addHandler(NullHandler())

__all__ = [
    "Engine",
    "EngineBuilder",
    "EngineConfig",
    "RunReport",
    "RunRequest",
    "StepReport",
    "__version__",
]
