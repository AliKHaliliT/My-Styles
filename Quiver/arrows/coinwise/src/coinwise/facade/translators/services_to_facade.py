from coinwise.facade.schemas import StrategyReport
from coinwise.services.accumulation import DriftResult


def services_to_facade_strategy_report(result: DriftResult) -> StrategyReport:

    """

    Convert a services DriftResult to a facade StrategyReport.

    """

    return StrategyReport(
        rounded_total=result.rounded_total,
        exact_total=result.exact_total,
        drift=result.drift,
        tie_count=result.tie_count,
    )
