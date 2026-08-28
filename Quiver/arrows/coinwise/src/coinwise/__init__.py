from importlib.metadata import PackageNotFoundError, version
from logging import NullHandler, getLogger

from coinwise.facade.experiment import grid_amounts, run_drift_experiment
from coinwise.facade.schemas import ExperimentReport, StrategyReport

try:
    __version__ = version("coinwise")
except PackageNotFoundError:
    __version__ = "0.0.0"

getLogger("coinwise").addHandler(NullHandler())

__all__ = [
    "ExperimentReport",
    "StrategyReport",
    "__version__",
    "grid_amounts",
    "run_drift_experiment",
]
